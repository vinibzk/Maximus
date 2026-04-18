import time
import threading

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.table import Table
from rich.align import Align
from rich.live import Live
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn
from rich import box

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

from config import CLAP_WINDOW, MODEL, USERNAME

console = Console()

LOGO = """\
 ███╗   ███╗ █████╗ ██╗  ██╗██╗███╗   ███╗██╗   ██╗███████╗
 ████╗ ████║██╔══██╗╚██╗██╔╝██║████╗ ████║██║   ██║██╔════╝
 ██╔████╔██║███████║ ╚███╔╝ ██║██╔████╔██║██║   ██║███████╗
 ██║╚██╔╝██║██╔══██║ ██╔██╗ ██║██║╚██╔╝██║██║   ██║╚════██║
 ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗██║██║ ╚═╝ ██║╚██████╔╝███████║
 ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝"""

TAG_COLORS = {
    "OK":   "bright_green",
    "SYS":  "magenta",
    "INFO": "cyan",
    "WARN": "yellow",
    "ERR":  "red",
}

def _now():
    return time.strftime("%H:%M:%S")

def log(tag: str, msg: str):
    color = TAG_COLORS.get(tag.upper(), "green")
    console.print(
        f"  [dim green][{_now()}][/dim green] "
        f"[dim green][[/dim green][{color}]{tag.upper()}[/{color}][dim green]][/dim green] "
        f"[dim white]{msg}[/dim white]"
    )

def _system_stats():
    if not HAS_PSUTIL:
        return "CPU: N/A  RAM: N/A"
    cpu = psutil.cpu_percent(interval=0.3)
    ram = psutil.virtual_memory().percent
    dsk = psutil.disk_usage('/').percent
    return f"CPU: {cpu:.0f}%  RAM: {ram:.0f}%  DISCO: {dsk:.0f}%"

def show_start():
    console.clear()
    console.print(Align.center(Text(LOGO, style="bold green")))
    console.print(Align.center(
        Text("ARTIFICIAL INTELLIGENCE ASSISTANT  •  v2.5.0  •  WINDOWS", style="dim green")
    ))
    console.print()

    stats = _system_stats()
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 3), expand=True)
    table.add_column(justify="left")
    table.add_column(justify="left")
    table.add_column(justify="left")
    table.add_column(justify="left")
    table.add_row(
        Text("◈ MODELO",   style="dim green"),
        Text(f"{MODEL} :: LOCAL",  style="bold green"),
        Text("◈ OLLAMA",   style="dim green"),
        Text("RUNNING :11434",     style="bold green"),
    )
    table.add_row(
        Text("◈ USER",     style="dim green"),
        Text(USERNAME,             style="bold green"),
        Text("◈ SISTEMA",  style="dim green"),
        Text(stats,                style="bold green"),
    )
    console.print(Panel(table, border_style="dark_green", box=box.SQUARE))
    console.print(Rule(style="dark_green"))

    boot_lines = [
        ("SYS",  "Maximus AI inicializando..."),
        ("OK",   f"Ollama conectado em localhost:11434"),
        ("OK",   f"Modelo {MODEL} carregado com sucesso"),
        ("OK",   f"Stream de áudio ativo — THRESHOLD: 0.03"),
        ("OK",   f"Sistema: {stats}"),
        ("INFO", f"Olá {USERNAME}! Aguardando 2 palmas para ativar..."),
    ]
    for tag, msg in boot_lines:
        log(tag, msg)
        time.sleep(0.25)

    console.print(Rule(style="dark_green"))
    show_listening()

def show_listening():
    console.print()
    console.print(Align.center(
        Text(f"◉  ESCUTANDO PALMAS  [ 0 / 2 ]  —  {int(CLAP_WINDOW)}s após 1ª palma", style="dim green")
    ))
    console.print()

def show_countdown():
    """Countdown visual após 1ª palma detetada."""
    console.print()
    log("INFO", "1ª palma detetada — bate a 2ª palma!")

    progress = Progress(
        TextColumn("  [cyan]⏱  AGUARDANDO 2ª PALMA[/cyan]"),
        BarColumn(bar_width=30, style="green", complete_style="bright_green"),
        TextColumn("[green]{task.fields[secs]}s[/green]"),
        console=console,
        transient=True,
    )

    total = int(CLAP_WINDOW)
    with progress:
        task = progress.add_task("", total=total, secs=total)
        for i in range(total):
            time.sleep(1)
            remaining = total - i - 1
            progress.update(task, advance=1, secs=remaining)

def show_done():
    console.print()
    console.print(Rule(style="green"))
    console.print(Align.center(
        Text("⚡  2 PALMAS DETETADAS  —  ATIVANDO SISTEMAS", style="bold green")
    ))
    console.print(Rule(style="green"))
    for tag, msg in [
        ("OK",   "Wake lock ativado"),
        ("OK",   "Spotify lançado"),
        ("OK",   "Browser lançado"),
        ("SYS",  "Trazendo terminal para frente..."),
        ("INFO", "Iniciando chat"),
    ]:
        log(tag, msg)
        time.sleep(0.15)
    console.print()

def show_done_timeout():
    console.print()
    console.print(Rule(style="yellow"))
    console.print(Align.center(
        Text("⏱  30s ESGOTADOS  —  ABRINDO APENAS O CHAT", style="bold yellow")
    ))
    console.print(Rule(style="yellow"))
    log("INFO", "Iniciando chat")
    console.print()

def show_chat_header():
    console.print(Panel(
        Align.center(Text(f"MAXIMUS ❯ CHAT ATIVO  •  {USERNAME}", style="bold green")),
        border_style="dark_green",
        box=box.SQUARE,
        subtitle="[dim green]'sair' para encerrar  •  '!help' para comandos[/dim green]",
    ))
    console.print()