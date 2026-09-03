from pathlib import Path
import ast, re

ROOT=Path(__file__).parents[1]
APP=(ROOT/"primebeats/app.py").read_text(encoding="utf-8")
FEATURES=(ROOT/"primebeats/features.py").read_text(encoding="utf-8")

def test_compile_tree():
    for p in ROOT.rglob("*.py"):
        ast.parse(p.read_text(encoding="utf-8"))

def test_player_callbacks_exist():
    for name in ("ping", "seek:", "refresh", "effect:", "auto", "favorite"):
        assert name in APP

def test_discovery_is_bounded():
    yt=(ROOT/"primebeats/youtube.py").read_text(encoding="utf-8")
    assert "Semaphore(4)" in yt
    assert "ytsearch" in yt

def test_effect_speed_chain_guard():
    app=ast.parse(APP)
    assert "_atempo_chain" in APP
    assert "0.5" in APP and "2.0" in APP

def test_known_command_collisions_removed():
    # These commands previously had duplicate handlers in the V7 alias layer.
    alias_line=next(x for x in APP.splitlines() if 'for alias,target in {' in x)
    for bad in ('"q":', '"qinfo":', '"info":', '"random":', '"charts":', '"top":', '"mix":', '"nonstop":'):
        assert bad not in alias_line
    assert 'if alias == "radio": alias = "radiofx"' in APP

def test_feature_matrix_nonempty():
    assert 'FEATURES = [' in FEATURES


def test_video_format_requires_audio_and_video():
    yt=(ROOT/"primebeats/youtube.py").read_text(encoding="utf-8")
    assert "vcodec!=none" in yt and "acodec!=none" in yt


def test_search_callback_keys_are_opaque_and_short():
    assert 'secrets.token_urlsafe(9)' in APP
    assert 'callback_data=f"searchplay:{key}:{i-1}"' in APP

def test_clone_storage_does_not_use_token_as_key():
    clone=(ROOT/"primebeats/clone.py").read_text(encoding="utf-8")
    assert 'self.clients.append(client)' in clone
    assert 'self.clients[token]' not in clone

def test_stream_state_commits_after_play():
    # Regression guard: assignment to current must occur after calls.play.
    assert APP.index('await asyncio.wait_for(maybe(self.calls.play(chat_id,media)), timeout=35)') < APP.index('p.current=track; p.paused=False; p.muted=False; p.video=bool(video); p.effect=effect_key')


def test_native_call_operations_are_bounded():
    src=(ROOT/'primebeats'/'app.py').read_text(encoding='utf-8')
    assert 'wait_for(maybe(self.calls.play(chat_id,media)), timeout=35)' in src
    # No direct unbounded leave_call awaits should remain.
    import re
    bad=re.findall(r'await maybe\(self\.calls\.leave_call\(', src)
    assert not bad

def test_user_stream_starts_are_bounded():
    src=(ROOT/'primebeats'/'app.py').read_text(encoding='utf-8')
    assert 'wait_for(self.stream(m.chat.id,track,video,p.effect), timeout=45)' in src


def test_clone_shutdown_iterates_list():
    clone=(ROOT/"primebeats/clone.py").read_text(encoding="utf-8")
    assert 'for c in list(self.clients):' in clone
    assert 'self.clients.values()' not in clone

def test_next_track_cleans_up_active_call_first():
    src=(ROOT/"primebeats/app.py").read_text(encoding="utf-8")
    leave=src.index('await asyncio.wait_for(maybe(self.calls.leave_call(chat_id)), timeout=5)', src.index('async def play_next'))
    play=src.index('await asyncio.wait_for(self.stream(chat_id,nxt', src.index('async def play_next'))
    assert leave < play

def test_play_requests_are_serialized_per_chat():
    src=(ROOT/"primebeats/app.py").read_text(encoding="utf-8")
    start=src.index('async def handle_play')
    end=src.index('async def reapply_effect', start)
    block=src[start:end]
    assert 'async with p.lock:' in block
    assert 'await asyncio.wait_for(self.stream(m.chat.id,track,video,p.effect), timeout=45)' in block
