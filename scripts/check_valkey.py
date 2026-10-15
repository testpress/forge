"""Exercise Forge's Redis clients against a running Valkey service."""

import asyncio
import os
from uuid import uuid4

import dramatiq
import redis
from channels_redis.core import RedisChannelLayer
from dramatiq.brokers.redis import RedisBroker
from dramatiq.worker import Worker

VALKEY_PORT = int(os.environ.get("VALKEY_PORT", "6379"))


def check_tasks() -> None:
    client = redis.Redis(host="localhost", port=VALKEY_PORT)
    assert client.ping()
    namespace = f"forge-smoke-{uuid4().hex}"
    result_key = f"{namespace}:result"
    broker = RedisBroker(client=client, namespace=namespace)

    @dramatiq.actor(broker=broker, max_retries=0)
    def record_result(value: str) -> None:
        client.rpush(result_key, value)
        client.expire(result_key, 60)

    worker = Worker(broker, worker_threads=1)
    worker.start()
    try:
        record_result.send("processed")
        result = client.blpop(result_key, timeout=15)
        assert result == (result_key.encode(), b"processed"), result
        broker.join(record_result.queue_name, timeout=15000)
    finally:
        worker.stop()
        broker.flush_all()
        client.delete(result_key)
        broker.close()
        client.close()


async def check_channels() -> None:
    layer = RedisChannelLayer(
        hosts=[("localhost", VALKEY_PORT)],
        prefix=f"forge-smoke-{uuid4().hex}",
    )
    try:
        channel = await layer.new_channel()
        await layer.group_add("smoke", channel)
        await layer.group_send(
            "smoke", {"type": "smoke.message", "value": "ok"}
        )
        message = await asyncio.wait_for(layer.receive(channel), timeout=5)
        assert message == {"type": "smoke.message", "value": "ok"}, message
        await layer.group_discard("smoke", channel)
    finally:
        await layer.flush()
        await layer.close_pools()


if __name__ == "__main__":
    check_tasks()
    asyncio.run(check_channels())
    print(
        "Valkey: Dramatiq task processing and Channels group messaging passed."
    )
