from __future__ import annotations
import asyncio, json, os
from dataclasses import asdict
from .state import Track

class LibraryStore:
    """Tiny JSON library for favorites/playlists. Metadata only; streams are refreshed on playback."""
    def __init__(self, path="data/library.json"):
        self.path = path
        self.lock = asyncio.Lock()
        self.data = {"favorites": {}, "playlists": {}}
        self._load()

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw=json.load(f)
            if isinstance(raw, dict): self.data.update(raw)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass

    async def _save(self):
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        tmp=self.path+".tmp"
        with open(tmp,"w",encoding="utf-8") as f: json.dump(self.data,f,ensure_ascii=False,indent=2)
        os.replace(tmp,self.path)

    async def favorite(self, user_id:int, track:Track):
        async with self.lock:
            key=str(user_id); self.data.setdefault("favorites",{}).setdefault(key,[])
            arr=self.data["favorites"][key]
            if not any(x.get("webpage_url")==track.webpage_url for x in arr): arr.insert(0,asdict(track)); arr[:50]
            self.data["favorites"][key]=arr[:50]; await self._save()

    async def unfavorite(self, user_id:int, webpage_url:str):
        async with self.lock:
            key=str(user_id); arr=self.data.setdefault("favorites",{}).get(key,[])
            self.data["favorites"][key]=[x for x in arr if x.get("webpage_url")!=webpage_url]
            await self._save()

    def favorites(self,user_id:int): return self.data.setdefault("favorites",{}).get(str(user_id),[])[:]

    async def playlist_add(self,user_id:int,name:str,track:Track):
        async with self.lock:
            key=str(user_id); playlists=self.data.setdefault("playlists",{}).setdefault(key,{})
            arr=playlists.setdefault(name[:40],[])
            if not any(x.get("webpage_url")==track.webpage_url for x in arr): arr.append(asdict(track))
            playlists[name[:40]]=arr[:100]; await self._save()

    def playlists(self,user_id:int): return self.data.setdefault("playlists",{}).get(str(user_id),{})
