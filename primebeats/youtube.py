from __future__ import annotations
import asyncio, re, os
from typing import Iterable
import yt_dlp
from .state import Track

BASE={
    "quiet":True,"no_warnings":True,"noplaylist":True,"skip_download":True,
    "format":"bestaudio[acodec!=none]/bestaudio/best","extract_flat":False,
    "socket_timeout":12,"retries":3,"fragment_retries":3,"concurrent_fragment_downloads":4,
}
COOKIE_FILE=os.getenv("YOUTUBE_COOKIES_FILE", "cookies.txt")
if os.path.isfile(COOKIE_FILE):
    BASE["cookiefile"] = COOKIE_FILE

# Curated anchors are only the starting point. Autoplay also performs live YouTube discovery,
# so a topic can continue beyond this list instead of stopping after a handful of seeds.
GENRE_SEEDS={
"romantic hindi":["Bairan Ishq Ve","Ishqa Ve","O Maahi","Heeriye","Sajni","Apna Bana Le","Tum Se Hi","Tera Ban Jaunga","Hawayein","Agar Tum Saath Ho","Ranjha","Ve Kamleya","Chaleya","Satranga","Tere Vaaste","Tum Kya Mile"],
"hindi romantic":["Bairan Ishq Ve","Ishqa Ve","O Maahi","Heeriye","Sajni","Apna Bana Le","Tum Se Hi","Tera Ban Jaunga","Hawayein","Agar Tum Saath Ho","Ranjha","Ve Kamleya","Chaleya","Satranga","Tere Vaaste","Tum Kya Mile"],
"lofi hindi":["Hindi Lofi Mix","Bollywood Lofi","Arijit Singh Lofi","Hindi Chill Mix","Rainy Hindi Lofi"],
"bollywood":["Bollywood Hits","Hindi New Songs","Bollywood Party Hits","Hindi Top Songs"],
"punjabi":["Punjabi Hits","Punjabi Romantic Songs","Punjabi Party Hits","New Punjabi Songs"],
"sad hindi":["Sad Hindi Songs","Arijit Singh Sad Songs","Heartbreak Hindi Songs","Hindi Sad Mix"],
"english pop":["Top English Pop Hits","English Chill Pop","Pop Hits Mix","Trending English Songs"],
}

def _extract(target,requested_by,video=False):
    q=target.strip()
    if not re.match(r"^https?://",q): q="ytsearch1:"+q
    opts=dict(BASE)
    opts["format"]=("best[height<=720][vcodec!=none][acodec!=none]/best[height<=720]/best" if video else "bestaudio[acodec!=none]/best[acodec!=none]/bestaudio/best")
    with yt_dlp.YoutubeDL(opts) as ydl: info=ydl.extract_info(q,download=False)
    if info and "entries" in info: info=next((x for x in info["entries"] if x),None)
    if not info: raise ValueError("No result found")
    url=info.get("url")
    if url:
        if video and info.get("vcodec") in (None, "none"): url=None
        elif not video and info.get("acodec") in (None, "none"): url=None
    if not url:
        for f in reversed(info.get("requested_formats") or info.get("formats") or []):
            if not f.get("url"): continue
            if video and f.get("vcodec") not in (None,"none") and f.get("acodec") not in (None,"none"):
                url=f["url"]; break
            if not video and f.get("acodec") not in (None,"none"):
                url=f["url"]; break
    if not url: raise ValueError("No playable media stream")
    return Track((info.get("title") or "Unknown")[:200],info.get("webpage_url") or target,url,
                 int(info.get("duration") or 0),info.get("thumbnail") or "",requested_by,"YouTube")

async def resolve(query,requested_by,video=False):
    return await asyncio.to_thread(_extract,query,requested_by,video)

async def search_results(query, limit=8):
    return await asyncio.to_thread(_search_flat, query, max(1,min(int(limit),20)))

def _search_flat(query,limit=20):
    """Return lightweight search entries without resolving CDN URLs."""
    opts={"quiet":True,"no_warnings":True,"skip_download":True,"extract_flat":True,
          "noplaylist":True,"socket_timeout":10,"retries":2}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info=ydl.extract_info(f"ytsearch{max(1,min(limit,50))}:{query}",download=False)
    out=[]
    for x in (info.get("entries") or []):
        if not x: continue
        x=dict(x)
        if not x.get("webpage_url") and x.get("id"):
            x["webpage_url"]=f"https://www.youtube.com/watch?v={x['id']}"
        if not x.get("title"): x["title"]="Unknown"
        out.append(x)
    return out

def _extract_playlist(target, requested_by, limit=50):
    opts={"quiet":True,"no_warnings":True,"skip_download":True,"extract_flat":True,
          "noplaylist":False,"playlistend":max(1,min(int(limit),100)),"socket_timeout":12,"retries":2}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info=ydl.extract_info(target,download=False)
    entries=[]
    for x in (info.get("entries") or []):
        if not x: continue
        url=(x.get("webpage_url") or x.get("url") or "").strip()
        title=(x.get("title") or "Unknown").strip()
        if url and title and not url.startswith("ytsearch"):
            entries.append(Track(title[:200],url,url,int(x.get("duration") or 0),x.get("thumbnail") or "",
                                  requested_by, "YouTube", False))
    return entries

async def resolve_playlist(target, requested_by, limit=50):
    return await asyncio.to_thread(_extract_playlist,target,requested_by,limit)

async def discover_topic(topic:str, requested_by:str="♾ Autoplay", limit:int=18,
                         exclude:Iterable[str]|None=None, round_no:int=0):
    """Continuously discover fresh tracks for a topic.

    It combines curated anchors with several live YouTube search phrases. This is deliberately
    not limited to the seed list, so autoplay can keep finding new songs indefinitely.
    """
    topic=topic.strip()[:120]
    excluded={str(x).strip().lower() for x in (exclude or []) if x}
    seeds=topic_seeds(topic)
    variants=[
        topic, f"{topic} songs", f"{topic} best songs", f"{topic} hits",
        f"{topic} playlist", f"{topic} mix", f"{topic} new songs",
        f"{topic} top songs", f"{topic} full playlist", f"{topic} popular songs",
        f"{topic} latest songs", f"{topic} evergreen songs", f"{topic} classics",
        f"{topic} albums", f"{topic} singles", f"{topic} artist songs",
        f"{topic} jukebox", f"{topic} nonstop", f"{topic} collection",
        f"{topic} all songs", f"{topic} playlist 2026",
        f"{topic} official audio", f"{topic} full album", f"{topic} album songs",
        f"{topic} female songs", f"{topic} male songs", f"{topic} duet songs",
        f"{topic} acoustic", f"{topic} live", f"{topic} classics",
    ]
    # Rotate search variants on later rounds. Every round still gets a curated anchor.
    shift=(round_no*5)%len(variants)
    variants=variants[shift:]+variants[:shift]
    queries=[]
    if seeds:
        queries.extend(seeds[:min(5,len(seeds))])
    queries.extend(variants[:8])

    out=[]; seen=set(excluded)
    sem=asyncio.Semaphore(4)
    async def one(q):
        async with sem:
            try: return await asyncio.to_thread(_search_flat,q,max(8,min(20,limit)))
            except Exception: return []
    # Bounded fan-out is intentionally used instead of firing every query at once; this
    # reduces transient throttling and keeps the bot responsive on smaller VPSs.
    results=await asyncio.gather(*(one(q) for q in queries),return_exceptions=True)
    for batch in results:
        if isinstance(batch,Exception): continue
        for x in batch:
            url=(x.get("webpage_url") or x.get("url") or "").strip()
            title=(x.get("title") or "Unknown").strip()
            if not url or not title or url.startswith("ytsearch"):
                continue
            key=url.lower()
            if key in seen: continue
            # Ignore obvious non-song junk for music autoplay.
            low=title.lower()
            if any(bad in low for bad in ("reaction", "shorts #", "trailer reaction")):
                continue
            seen.add(key)
            out.append(Track(title[:200],url,url,int(x.get("duration") or 0),x.get("thumbnail") or "",requested_by,"YouTube"))
            if len(out)>=limit: return out
    return out

def duration(sec):
    if not sec:return "LIVE"
    m,s=divmod(int(sec),60);h,m=divmod(m,60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def topic_seeds(topic):
    key=topic.strip().lower()
    for k,v in GENRE_SEEDS.items():
        if k in key or key in k:return v[:]
    return [f"{topic} best songs",f"{topic} hits",f"{topic} mix",f"{topic} playlist"]
