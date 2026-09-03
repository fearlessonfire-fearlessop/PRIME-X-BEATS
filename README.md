# ⚝ PRIME × BEATS !!

Production-oriented Telegram Voice Chat music/video bot with a hacker/pro UI, safe playback recovery, continuous discovery autoplay, HD video profile, effects, libraries, approvals and cloning.

## ⚡ OMEGA improvements / bug fixes
- Functional ±20s seek controls with safe clean restart
- No duplicate `/radio` vs Radio-FX command collision
- No duplicate queue/search/discovery alias handlers
- Callback ping now has a real response
- Position-preserving effect/speed/refresh restarts
- FFmpeg `atempo` chaining that stays within valid per-filter limits
- Bounded YouTube discovery concurrency to reduce throttling
- Search result URL normalization for reliable playback
- Three-attempt playback recovery + timeouts
- Failed-track isolation and automatic continuation
- Callback ping + stale callback feedback
- VC auto-leave when enabled and playback is exhausted
- Version/Owner/Support dashboards
- 39+ fixed audio effects
- Audio VC + HD 720p video profile
- YouTube playlist import, search and inline search
- Favorites and personal playlists
- Owner approval gate and admin controls

## ♾ Infinite-style autoplay
`/autoplay Romantic Hindi Songs` combines curated anchors with many rotating live YouTube search queries. It deduplicates current/queue/history/seen URLs and refills the queue in the background.

It can continue discovering matching results for a long time, but no bot can literally guarantee every recording on the internet because there is no universal catalog and external search results change.

## 🎵 Examples
```bash
/play One Love - Shubh
/vplay Bairan
/autoplay Romantic Hindi Songs
/radio Romantic Hindi Songs
/discover Bollywood classics
/search Bairan
/playlist <YouTube playlist URL>
```

## 🎛 Effects
Normal, No Vocals, Slowed, Deep Slowed, Slowed + Reverb, Daycore, Speed Up, Nightcore, Hyperpop, Bass Boost, Super Bass, Concert Hall, Grand Hall, Cathedral, Studio Reverb, Club Reverb, 8D, 3D, Stereo Panner, Phaser, Chorus, Vaporwave, Lo-Fi, 8-Bit, Radio, Treble, Pitch Down, Pitch Up, Underwater, Vocal Boost, Mono, Wide Stereo, Telephone, Vinyl, Compressor, Tremolo, Echo, Deep Bass, Air.

## 🔐 Setup
Required environment variables:
```text
API_ID=
API_HASH=
BOT_TOKEN=
ASSISTANT_SESSION=
OWNER_ID=7915543522
```

Generate the assistant session locally with `python tools/generate_session.py`. Never send Telegram login OTPs or session strings to a bot chat.

## 🐳 Docker
```bash
docker build -t prime-beats .
docker run --env-file .env prime-beats
```

## 🧪 Validation
Run `python -m compileall -q primebeats` and `python -m unittest`/your CI runner. The included regression suite checks syntax, callback coverage, discovery throttling and command-collision regressions. A live Telegram VC smoke test still requires real credentials, a real assistant account, an active VC and network access.

Runtime failures outside the code (Telegram permissions/call state, YouTube availability, CDN/network or hosting) cannot be mathematically eliminated; V8 focuses on graceful recovery instead of false zero-error claims.

## 🏆 OMEGA production target
OMEGA is the cleaned production baseline for PRIME × BEATS. It prioritizes fast async handling, bounded discovery, state-safe playback restarts, recovery, permissions and a dense Telegram-native UI. Telegram Mini Apps can be layered on later for a full visual dashboard, while the core bot remains usable without one.

### Autoplay philosophy
`/autoplay <topic>` is an open-ended discovery mode. It combines seed tracks, rotating search patterns, deduplication and background queue refill. It cannot promise every recording on the internet because external catalogs and availability are not exhaustive.


### Optional YouTube cookies

Place a Netscape-format `cookies.txt` in the project root (never commit it), or set `YOUTUBE_COOKIES_FILE` to a private path. The resolver uses it automatically when the file exists.
