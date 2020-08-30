import asyncio
import importlib
import logging
import typing as t
import time
import os

import server

from concurrent.futures import ProcessPoolExecutor, Future


SHARD_COUNT = 6
WORKERS = 2
IPC_PORT = 8080
BOT_PATH = "auto_voice_channels.avc:start_bot_cluster"
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

logging.basicConfig(level=logging.INFO)


def shard_ids_from_cluster(cluster: int, per: int):
    return list(range(per * cluster, per * cluster + per))


class Manager(server.Server):
    def __init__(self, shard_count: int, worker_count: int, icp_port: int, bot_path: str):
        super().__init__(icp_port)

        self._shards = shard_count
        self._workers = worker_count

        self._cluster_packs = [
            shard_ids_from_cluster(c_id, self._shards // 2) for c_id in range(self._workers)]

        module, attr = bot_path.split(":", maxsplit=1)
        self._avc = importlib.import_module(module)
        self._starter: t.Callable = getattr(self._avc, attr)
        if self._starter is None:
            raise ImportError("Could not import and extract bot: {} from file: {}".format(attr, module))

        self._pool: t.Optional[ProcessPoolExecutor] = None
        self._active_proc: t.List[Future] = []

        self.logger = logging.getLogger("avc-shard-manager")

    def create_pool(self):
        self._pool = ProcessPoolExecutor(max_workers=self._workers)
        self.logger.debug("Successfully created process pool of %s workers", str(self._workers))

    def shutdown_pool(self):
        if self._pool is not None:
            self._pool.shutdown()
        self.logger.debug("Process pool has been shutdown")

    def _spawn_workers(self, token: str, *args, **kwargs):
        if self._pool is None:
            raise RuntimeError("Process pool has not been initialised yet!")

        for cluster_id, shards in enumerate(self._cluster_packs):
            future = self._pool.submit(self._starter, token, cluster_id, shards, *args, **kwargs)
            self._active_proc.append(future)
            self.logger.info("Created cluster with id: %s", str(cluster_id))
            time.sleep(2)

    async def _start(self, token: str, *args, **kwargs):
        self._spawn_workers(token, *args, **kwargs)

    def start(self, token: str, *args, **kwargs):
        asyncio.get_event_loop().run_until_complete(self._start(token, *args, **kwargs))

    def __enter__(self):
        self.create_pool()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("Cancelling pending processes...")
        for fut in self._active_proc:
            if not fut.done():
                fut.cancel()
        self.logger.info("Cancel succeeded")
        self.shutdown_pool()
        self.logger.info("Pool shutdown successfully.")


if __name__ == '__main__':
    with Manager(
            shard_count=SHARD_COUNT, worker_count=WORKERS, icp_port=IPC_PORT, bot_path=BOT_PATH) as m:
        m.start(token=BOT_TOKEN)
