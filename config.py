import os
from dotenv import load_dotenv

load_dotenv()

THRESHOLD    = float(os.getenv("THRESHOLD",   "0.03"))
CLAP_WINDOW  = float(os.getenv("CLAP_WINDOW", "30"))
MODEL        = os.getenv("MODEL",        "llama3.2")
OLLAMA_URL   = os.getenv("OLLAMA_URL",   "http://localhost:11434/api/chat")
SPOTIFY_URI  = os.getenv("SPOTIFY_URI",  "spotify:track:08mG3Y1vljYA6bvDt4Wqkj")
USERNAME     = os.getenv("USERNAME",     "Guide")
MAX_HISTORY  = int(os.getenv("MAX_HISTORY", "20"))
TIMEOUT      = int(os.getenv("TIMEOUT",     "60"))