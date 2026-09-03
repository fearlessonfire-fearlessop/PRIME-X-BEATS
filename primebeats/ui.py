from __future__ import annotations
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .youtube import duration
from .effects import EFFECTS
import time

def esc(s:str)->str:
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def links(cfg):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 Owner",url="https://t.me/Prime_Fearless_45"),
         InlineKeyboardButton("💬 Support Group",url="https://t.me/SPARK_X_NETWORK")],
        [InlineKeyboardButton("📢 Support Channel",url="https://t.me/SPARK_X_NETWORK_OP"),
         InlineKeyboardButton("⚡ Official Fearless",url="https://t.me/Prime_Arrived")]
    ])

def home_keyboard(cfg):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎧 PLAY",callback_data="help:play"),InlineKeyboardButton("📜 QUEUE",callback_data="queue")],
        [InlineKeyboardButton("▶ NOW PLAYING",callback_data="now"),InlineKeyboardButton("♾ AUTOPLAY",callback_data="auto")],
        [InlineKeyboardButton("⏸ PAUSE",callback_data="pause"),InlineKeyboardButton("⏭ SKIP",callback_data="skip"),InlineKeyboardButton("⏹ STOP",callback_data="stop")],
        [InlineKeyboardButton("🔀 SHUFFLE",callback_data="shuffle"),InlineKeyboardButton("🔁 LOOP",callback_data="loop")],
        [InlineKeyboardButton("🔊 VOL −",callback_data="voldown"),InlineKeyboardButton("🔊 VOL +",callback_data="volup"),InlineKeyboardButton("🔇 MUTE",callback_data="mute")],
        [InlineKeyboardButton("🎛 EFFECTS",callback_data="effects:0"),InlineKeyboardButton("📖 HELP",callback_data="help"),InlineKeyboardButton("⚡ PING",callback_data="ping")],
        [InlineKeyboardButton("🌐 Support & Links",callback_data="links")]
    ])

def player_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏸ Pause",callback_data="pause"),InlineKeyboardButton("▶ Resume",callback_data="resume"),InlineKeyboardButton("⏭ Skip",callback_data="skip"),InlineKeyboardButton("⏹ Stop",callback_data="stop")],
        [InlineKeyboardButton("« -20s",callback_data="seek:-20"),InlineKeyboardButton("🔄 Refresh",callback_data="refresh"),InlineKeyboardButton("+20s »",callback_data="seek:20")],
        [InlineKeyboardButton("⏮ Previous",callback_data="previous"),InlineKeyboardButton("📜 Queue",callback_data="queue"),InlineKeyboardButton("🔀 Shuffle",callback_data="shuffle")],
        [InlineKeyboardButton("🔁 Loop",callback_data="loop"),InlineKeyboardButton("⭐ Favorite",callback_data="favorite"),InlineKeyboardButton("🎚 Mode",callback_data="mode")],
        [InlineKeyboardButton("🎛 Audio Effects",callback_data="effects:0")],
        [InlineKeyboardButton("♾ Autoplay",callback_data="auto"),InlineKeyboardButton("🔉 −",callback_data="voldown"),InlineKeyboardButton("🔊 +",callback_data="volup")],
        [InlineKeyboardButton("🧹 Clear",callback_data="clear"),InlineKeyboardButton("⚡ Ping",callback_data="ping")]
    ])

def effects_keyboard(page=0):
    keys=list(EFFECTS.items()); per=10
    chunk=keys[page*per:(page+1)*per]
    rows=[]
    for i in range(0,len(chunk),2):
        row=[]
        for k,(label,_) in chunk[i:i+2]: row.append(InlineKeyboardButton(label,callback_data=f"effect:{k}"))
        rows.append(row)
    nav=[]
    if page>0: nav.append(InlineKeyboardButton("« Prev",callback_data=f"effects:{page-1}"))
    if (page+1)*per<len(keys): nav.append(InlineKeyboardButton("Next »",callback_data=f"effects:{page+1}"))
    if nav: rows.append(nav)
    rows.append([InlineKeyboardButton("↩ Back to Player",callback_data="now")])
    return InlineKeyboardMarkup(rows)

def welcome(cfg,user):
    return (
        f"<b>╭━━━〔 ⚝ {esc(cfg.bot_name)} 〕━━━╮</b>\n"
        "<b>┃ ⚡ ULTRA VOICE MUSIC ENGINE</b>\n"
        "<b>┃ 🎧 Audio • 🎥 Video • ♾ Autoplay</b>\n"
        "<b>┃ 🎛 39+ Audio FX • Smart Queue</b>\n"
        f"<b>┃ 👤 Welcome, {esc(user)}</b>\n"
        "<b>╰━━━━━━━━━━━━━━━━━━━━╯</b>\n\n"
        "<blockquote>⚡ <b>Fast. Clean. Responsive.</b>\n"
        "Built for Telegram Voice Chats.</blockquote>\n\n"
        "<b>🚀 QUICK START</b>\n<code>/approvegc</code> • Owner approval\n<code>/play O Maahi</code>\n<code>/vplay music video</code>\n<code>/autoplay Romantic Hindi Songs</code>\n<code>/radio Romantic Hindi Songs</code> • continuous discovery\n<code>/discover topic</code> • fill fresh results"
    )

def progress_bar(p, width=14):
    if not p.current or not p.current.duration or not p.started_at: return "LIVE"
    elapsed=max(0,int(time.monotonic()-p.started_at))
    elapsed=min(elapsed,int(p.current.duration))
    ratio=min(1,elapsed/max(1,p.current.duration))
    filled=int(width*ratio)
    return "━"*filled+"●"+"─"*(width-filled)+f" {elapsed//60}:{elapsed%60:02d}/{duration(p.current.duration)}"

def player_text(p,name):
    auto=f"ON • {esc(p.autoplay_topic)}" if p.autoplay and p.autoplay_topic else ("ON" if p.autoplay else "OFF")
    effect=getattr(p,"effect","normal")
    effect_name=EFFECTS.get(effect,("Normal",""))[0]
    if not p.current:
        return (f"<b>╭━━〔 ⚝ {esc(name)} 〕━━╮</b>\n"
                f"┃ 🟢 <b>PLAYER READY</b>\n┃ ♾ Auto: <code>{auto}</code>\n"
                f"┃ 🎛 FX: <code>{esc(effect_name)}</code>\n"
                f"┃ ⚡ Speed: <code>{getattr(p,'speed',1.0):.2f}x</code>\n"
                f"┃ 📚 Queue: <code>{len(p.queue)}</code>\n"
                f"<b>╰━━━━━━━━━━━━━━━━━━━━╯</b>")
    t=p.current
    mode="🎥 VIDEO" if getattr(p,"video",False) else "🎧 AUDIO"
    state="⏸ PAUSED" if p.paused else "▶️ PLAYING"
    return f"<b>╭━━〔 ⚝ {esc(name)} 〕━━╮</b>\n┃ {state} • {mode}\n┃ 🎵 <b>{esc(t.title)}</b>\n┃ ⏱ <code>{duration(t.duration)}</code>\n┃ 👤 {esc(t.requested_by)}\n┃ 🔊 <code>{p.volume}%</code> • 📚 <code>{len(p.queue)}</code>\n┃ 🎛 {esc(effect_name)}\n┃ 🔁 Loop: <code>{'ON' if p.loop else 'OFF'}</code> • ♾ Auto: <code>{auto}</code>\n<b>╰━━━━━━━━━━━━━━━━━━━━╯</b>"

def help_text(name):
    return f"""<b>⚝ {esc(name)} • COMMAND MATRIX</b>

<b>🎧 PLAYBACK</b>
<code>/play</code> <code>/vplay</code> <code>/pause</code> <code>/resume</code> <code>/skip</code> <code>/stop</code>
<code>/queue</code> <code>/now</code> <code>/clear</code> <code>/remove 2</code> <code>/jump 3</code>
<code>/shuffle</code> <code>/loop</code> <code>/volume 0-200</code> <code>/mute</code> <code>/unmute</code>
<code>/seek 30</code> <code>/seekback 20</code> <code>/speed 1.1</code> <code>/previous</code> <code>/replay</code>

<b>♾ AUTOPLAY</b>
<code>/autoplay Romantic Hindi Songs</code>
<code>/radio Romantic Hindi Songs</code> • continuous discovery
<code>/discover topic</code> • fill fresh results
<code>/autoplay off</code> <code>/autoplay next</code>

<b>🎛 EFFECTS</b>
<code>/effect bass_boost</code> • 30+ presets
Normal • No Vocals • Slowed • Deep Slowed • Slowed+Reverb • Daycore • Nightcore • Hyperpop • Bass Boost • Super Bass • Hall/Reverb • 8D • 3D • Phaser • Chorus • Vaporwave • Lo-Fi • Radio • Treble • Pitch • Underwater

<b>🛠 DISCOVERY & TOOLS</b>
<code>/search song</code> <code>/discover topic</code> <code>/radio topic</code>
<code>/ping</code> <code>/stats</code> <code>/history</code> <code>/health</code> <code>/settings</code> <code>/features</code>

<b>👑 OWNER</b>
<code>/approvegc</code> <code>/revoke_gc</code> <code>/clone</code> <code>/clones</code>

<blockquote>🛡 Playback is locked until the main owner approves the group.
⚡ Autoplay uses curated + live discovery and keeps refilling the queue.</blockquote>"""
