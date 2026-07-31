import redis.asyncio
import json

class MessageBroker():
    def __init__(self):
        self.r = redis.asyncio.Redis(
                    host='localhost', 
                    port=6379,
                    decode_responses=True
                    )
    
    async def publishMessage(self, chanel, value):
        value = json.dumps(value, separators=(',', ':'), ensure_ascii=False)
        if self.r:
            await self.r.publish(chanel, value)

    async def subscribe(self, chanel, callback):
        pubsub = self.r.pubsub()
        await pubsub.subscribe(chanel)
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = message["data"]
                await callback(data)

        
        pass