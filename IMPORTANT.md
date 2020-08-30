# Please Note branch is for production.<br> DO NOT USE THIS FOR YOUR SELF HOSTED BOTS!
This version is designed to spread the bot load across multiple cores, this has a 
some negative impact on small bots because of the extra overhead.<br>
**DO NOT USE THIS FOR YOUR SELF HOSTED BOTS!**

## Some needed info
- The file scale_start.py should be what you use to start the bot.
- Any modification of shards or processes should be set in `scale_start.py`
- Any sharding notes set in the `avc.py` file will be overwritten.
- If you set too many shards for guilds you will stop shards like flies make sure you 
are aware of this before doing 12 processes and 400 shards per processes :P
- Shard counts are done by `SHARDS_PER_CLUSTER` not as a total amount, its just easier this way.
- Each process is stateful, meaning it knows what it is, e.g cluster `0`

**Example Config:**

```python
import os

SHARDS_PER_CLUSTER = 1
WORKERS = 1
IPC_PORT = 8080
BOT_PATH = "auto_voice_channels.avc:start_bot_cluster"
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
```

This is create a total of `1` shards because `1 * 1 = 1` *magic i know.*<br>
`IPC_PORT` represents the port the websocket binds to so the processes can have some IPC.
