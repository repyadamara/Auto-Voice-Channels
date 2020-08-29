import asyncio

from concurrent.futures import ProcessPoolExecutor


SHARD_COUNT = 6
WORKERS = 2
IPC_PORT = 8080
BOT_PATH = "auto_voice_channels.avc:"


def shard_ids_from_cluster(cluster: int, per: int):
    return list(range(per * cluster, per * cluster + per))


class Manager:
    def __init__(self, shard_count: int, worker_count: int, icp_port: int):
        self.shards = shard_count
        self.workers = worker_count
        self.port = icp_port

        self._cluster_packs = [
            shard_ids_from_cluster(c_id, SHARD_COUNT // 2) for c_id in range(WORKERS)]

    def _spawn_workers



