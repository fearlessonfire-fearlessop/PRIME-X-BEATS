from __future__ import annotations
import asyncio
from pyrogram import Client
from pyrogram.errors import RPCError

class CloneManager:
    def __init__(self, api_id: int, api_hash: str, owner_id: int):
        self.api_id, self.api_hash, self.owner_id = api_id, api_hash, owner_id
        self.clients: list[Client] = []

    async def create(self, token: str):
        token = (token or "").strip()
        if not token or ":" not in token or len(token) < 20 or len(token) > 256:
            raise ValueError("Invalid bot token format")
        client = Client(
            f"clone_{len(self.clients)+1}",
            api_id=self.api_id,
            api_hash=self.api_hash,
            bot_token=token,
            in_memory=True,
        )
        await client.start()
        me = await client.get_me()
        self.clients.append(client)
        return me

    async def stop_all(self):
        for c in list(self.clients):
            try: await c.stop()
            except Exception: pass
        self.clients.clear()
