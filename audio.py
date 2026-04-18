import sounddevice as sd
import numpy as np
import time
import threading

THRESHOLD   = 0.03
CLAP_GAP    = 1.0
CLAP_WINDOW = 30.0

_lock         = threading.Lock()
_last_time    = 0.0
_count        = 0
_window_timer = None
_paused       = False   # ← quando True, ignora todo o áudio

on_clap_trigger         = None
on_clap_timeout_trigger = None

def pause():
    """Para a deteção de palmas (ex: durante o chat)."""
    global _paused
    with _lock:
        _paused = True
        _reset_state()

def resume():
    """Retoma a deteção de palmas."""
    global _paused
    with _lock:
        _paused = False

def _reset_state():
    """Limpa estado interno — deve ser chamado com _lock held."""
    global _last_time, _count, _window_timer
    _last_time = 0.0
    _count     = 0
    if _window_timer:
        _window_timer.cancel()
        _window_timer = None

def _handle_timeout():
    global _window_timer
    with _lock:
        if _paused:
            return
        _reset_state()
    if on_clap_timeout_trigger:
        threading.Thread(target=on_clap_timeout_trigger, daemon=True).start()

def detect(indata):
    global _last_time, _count, _window_timer

    with _lock:
        if _paused:
            return

    volume = np.sqrt(np.mean(indata ** 2))
    if volume <= THRESHOLD:
        return

    now     = time.time()
    trigger = False

    with _lock:
        if _paused:
            return

        if now - _last_time < CLAP_GAP:
            return  # som contínuo — ignora

        _last_time = now
        _count += 1

        if _count == 1:
            if _window_timer:
                _window_timer.cancel()
            _window_timer = threading.Timer(CLAP_WINDOW, _handle_timeout)
            _window_timer.daemon = True
            _window_timer.start()

        elif _count >= 2:
            _reset_state()
            trigger = True

    if trigger and on_clap_trigger:
        threading.Thread(target=on_clap_trigger, daemon=True).start()

def audio_callback(indata, frames, time_info, status):
    # input overflow é normal em microfones lentos — suprime o aviso
    if status and "input overflow" not in str(status).lower():
        print(f"[AUDIO] {status}")
    detect(indata)

def start_listening():
    try:
        with sd.InputStream(
            callback=audio_callback,
            blocksize=4096,       # buffer maior → menos overflows
            latency="high",       # latência alta → mais tolerante
        ):
            while True:
                time.sleep(0.1)
    except Exception as e:
        print(f"[ERR] Stream de áudio falhou: {e}")