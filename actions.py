import sys
import time
import ctypes
import subprocess
import webbrowser
import ui
from config import SPOTIFY_URI

"""
def wake_pc():
    if sys.platform == "win32":
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
            ui.log("OK", "Wake lock ativado")
        except Exception as e:
            ui.log("WARN", f"Wake lock falhou: {e}")
"""

def abrir_spotify():
    try:
        subprocess.Popen(["start", SPOTIFY_URI], shell=True)
        ui.log("OK", "Spotify lançado")
    except Exception as e:
        ui.log("ERR", f"Erro ao abrir Spotify: {e}")

def abrir_instagram():
    try:
        webbrowser.open("https://instagram.com")
        ui.log("OK", "Browser lançado")
    except Exception as e:
        ui.log("ERR", f"Erro ao abrir Instagram: {e}")

def trazer_cmd_para_frente():
    if sys.platform != "win32":
        return
    try:
        time.sleep(2)
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 9)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            ui.log("OK", "Terminal trazido para frente")
    except Exception as e:
        ui.log("WARN", f"Não foi possível trazer terminal: {e}")

def executar():
    wake_pc()
    abrir_spotify()
    abrir_instagram()
    trazer_cmd_para_frente()