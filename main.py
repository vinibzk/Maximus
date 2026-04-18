import threading
import sys

import audio
import actions
import chat
import ui

_busy          = False
_busy_lock     = threading.Lock()
_countdown_thread = None

# ── Callbacks de áudio ────────────────────────────────────────────────────────

def on_first_clap():
    """1ª palma — mostra countdown visual (não bloqueia o áudio)."""
    global _countdown_thread
    _countdown_thread = threading.Thread(target=ui.show_countdown, daemon=True)
    _countdown_thread.start()

def on_clap():
    """2 palmas dentro do tempo — ativa tudo."""
    global _busy
    with _busy_lock:
        if _busy:
            return
        _busy = True
    threading.Thread(target=_handle_clap_full, daemon=True).start()

def on_clap_timeout():
    """30s sem 2ª palma — só chat."""
    global _busy
    with _busy_lock:
        if _busy:
            return
        _busy = True
    threading.Thread(target=_handle_clap_timeout, daemon=True).start()

# ── Handlers ──────────────────────────────────────────────────────────────────

def _handle_clap_full():
    global _busy
    try:
        ui.show_done()
        actions.executar()
        audio.pause()
        chat.iniciar_chat()
    except Exception as e:
        ui.log("ERR", f"Erro: {e}")
    finally:
        audio.resume()
        ui.show_listening()
        with _busy_lock:
            _busy = False

def _handle_clap_timeout():
    global _busy
    try:
        ui.show_done_timeout()
        audio.pause()
        chat.iniciar_chat()
    except Exception as e:
        ui.log("ERR", f"Erro: {e}")
    finally:
        audio.resume()
        ui.show_listening()
        with _busy_lock:
            _busy = False

# ── Debug mode ────────────────────────────────────────────────────────────────

def _debug_mode():
    import sounddevice as sd
    import numpy as np
    ui.log("INFO", "MODO DEBUG — mostrando volume do microfone (Ctrl+C para sair)")
    ui.log("INFO", f"THRESHOLD atual: {audio.THRESHOLD:.4f}")

    def cb(indata, *_):
        vol = float(np.sqrt(np.mean(indata ** 2)))
        bar = "█" * int(vol * 500)
        print(f"\r  VOL: {vol:.4f}  {bar:<40}", end="", flush=True)

    with sd.InputStream(callback=cb, blocksize=4096, latency="high"):
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            print()

# ── Main ──────────────────────────────────────────────────────────────────────

audio.on_first_clap           = on_first_clap
audio.on_clap_trigger         = on_clap
audio.on_clap_timeout_trigger = on_clap_timeout

def main():
    if "--debug" in sys.argv:
        _debug_mode()
        return

    ui.show_start()
    threading.Thread(target=audio.start_listening, daemon=True).start()

    stop = threading.Event()
    try:
        stop.wait()
    except KeyboardInterrupt:
        ui.log("SYS", "Encerrando Maximus...")

if __name__ == "__main__":
    main()