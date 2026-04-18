import json
import os
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
import requests
import ui
from config import MODEL, OLLAMA_URL, MAX_HISTORY, TIMEOUT, USERNAME, SPOTIFY_URI

MEMORY_DIR  = Path("memory")
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        f"És o Maximus, assistente pessoal inteligente e direto de {USERNAME}. "
        "Respondes sempre em português europeu. "
        "És conciso, útil e ligeiramente sarcástico quando adequado. "
        "Tens memória das conversas anteriores e usas esse contexto. "
        "Nunca digas que és uma IA a menos que te perguntem diretamente. "
        "Quando não souberes algo, admite sem rodeios."
    ),
}

COMMANDS = {
    "!help":     "Mostra esta lista de comandos",
    "!spotify":  "Abre o Spotify",
    "!instagram":"Abre o Instagram",
    "!memoria":  "Mostra ficheiros de memória guardados",
    "!limpar":   "Limpa a memória desta sessão",
    "!stats":    "Mostra estatísticas do sistema",
    "!horas":    "Mostra hora atual",
    "sair":      "Encerra o chat",
}

def _session_file():
    MEMORY_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return MEMORY_DIR / f"{stamp}.json"

def _load_last_session():
    if not MEMORY_DIR.exists():
        return []
    files = sorted(MEMORY_DIR.glob("*.json"), reverse=True)
    if not files:
        return []
    try:
        with open(files[0], "r", encoding="utf-8") as f:
            history = json.load(f)
        clean = [m for m in history if m.get("content", "").strip()]
        ui.log("INFO", f"Memória carregada: {files[0].name} ({len(clean)} mensagens)")
        return clean
    except Exception as e:
        ui.log("WARN", f"Erro ao carregar memória: {e}")
        return []

def _save_session(history, filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(history[-MAX_HISTORY:], f, ensure_ascii=False, indent=2)
    except Exception as e:
        ui.log("WARN", f"Erro ao guardar memória: {e}")

def _handle_command(cmd, history):
    """Retorna True se foi um comando especial."""
    c = cmd.strip().lower()

    if c == "!help":
        ui.console.print("\n  [dim green]Comandos disponíveis:[/dim green]")
        for k, v in COMMANDS.items():
            ui.console.print(f"  [green]{k:<12}[/green] [dim white]{v}[/dim white]")
        ui.console.print()
        return True

    if c == "!spotify":
        try:
            subprocess.Popen(["start", SPOTIFY_URI], shell=True)
            ui.log("OK", "Spotify aberto")
        except Exception as e:
            ui.log("ERR", str(e))
        return True

    if c == "!instagram":
        try:
            webbrowser.open("https://instagram.com")
            ui.log("OK", "Instagram aberto")
        except Exception as e:
            ui.log("ERR", str(e))
        return True

    if c == "!memoria":
        if not MEMORY_DIR.exists():
            ui.log("INFO", "Sem sessões guardadas")
        else:
            files = sorted(MEMORY_DIR.glob("*.json"), reverse=True)
            ui.console.print("\n  [dim green]Sessões guardadas:[/dim green]")
            for f in files[:10]:
                size = f.stat().st_size
                ui.console.print(f"  [green]{f.name}[/green] [dim white]{size} bytes[/dim white]")
            ui.console.print()
        return True

    if c == "!limpar":
        history.clear()
        ui.log("OK", "Memória desta sessão limpa")
        return True

    if c == "!stats":
        ui.log("INFO", ui._system_stats())
        return True

    if c == "!horas":
        ui.log("INFO", datetime.now().strftime("São %H:%M:%S de %d/%m/%Y"))
        return True

    return False

def iniciar_chat():
    history = _load_last_session()
    session_file = _session_file()

    ui.show_chat_header()

    while True:
        try:
            user = input("  MAXIMUS ❯ ").strip()
        except (EOFError, KeyboardInterrupt):
            ui.log("SYS", "Chat encerrado.")
            _save_session(history, session_file)
            break

        if not user:
            continue

        if user.lower() in ["sair", "exit", "quit"]:
            ui.log("SYS", "Encerrando chat...")
            _save_session(history, session_file)
            break

        if _handle_command(user, history):
            continue

        history.append({"role": "user", "content": user})

        try:
            messages = [SYSTEM_PROMPT] + history[-MAX_HISTORY:]
            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "messages": messages, "stream": True},
                stream=True,
                timeout=TIMEOUT,
            )
            response.raise_for_status()

            print("  [IA] ", end="", flush=True)
            full_response = ""

            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    print(token, end="", flush=True)
                    full_response += token
                    if chunk.get("done"):
                        break

            print("\n")
            history.append({"role": "assistant", "content": full_response})
            _save_session(history, session_file)

        except requests.exceptions.ConnectionError:
            ui.log("ERR", "Ollama não acessível — servidor a correr?")
        except requests.exceptions.Timeout:
            ui.log("ERR", f"Timeout após {TIMEOUT}s")
        except requests.exceptions.HTTPError as e:
            ui.log("ERR", f"HTTP {e.response.status_code}")
        except Exception as e:
            ui.log("ERR", f"Erro inesperado: {e}")