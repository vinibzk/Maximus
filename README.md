# Maximus
Assistente pessoal local para Windows ativado por palmas. Deteta 2 palmas via microfone, abre Spotify e browser, e inicia um chat com IA offline via Ollama (llama3.2). Terminal UI com ASCII art, memória por sessão e comandos integrados. 100% offline.

# MAXIMUS AI 🤖

> Assistente pessoal local ativado por palmas, com chat de IA offline via Ollama.

---

## O que é o Maximus?

O Maximus é um assistente pessoal para Windows que vive no terminal. Basta bater duas palmas para ele acordar — abre o Spotify, o browser e inicia uma conversa com um modelo de linguagem local (llama3.2 via Ollama). Tudo offline, sem custos por mensagem, sem cloud.

---

## Funcionalidades

- **Ativação por palmas** — deteta 2 palmas consecutivas via microfone
- **Janela de 30 segundos** — após a 1ª palma tens 30s para bater a 2ª; se não o fizeres, abre apenas o chat
- **Countdown visual** — barra de progresso em tempo real após a 1ª palma
- **Chat com IA local** — llama3.2 via Ollama, 100% offline
- **Personalidade** — o Maximus responde em português europeu com personalidade própria
- **Memória por sessão** — cada conversa é guardada em ficheiro separado com timestamp
- **Comandos especiais** — controlo direto via chat sem chamar o modelo
- **Stats do sistema** — CPU, RAM e disco no arranque via psutil
- **UI ASCII no terminal** — logo, painéis e logs coloridos com rich
- **Modo debug** — visualiza o volume do microfone em tempo real para calibrar o threshold
- **Configuração por `.env`** — todas as constantes num ficheiro editável

---

## Estrutura do projeto

```
Maximus/
├── main.py          # Entrada principal, orquestra todos os módulos
├── audio.py         # Deteção de palmas via microfone
├── chat.py          # Chat com Ollama + comandos especiais
├── actions.py       # Abre Spotify, Instagram, wake lock
├── ui.py            # Interface visual no terminal (rich)
├── config.py        # Carrega variáveis do .env
├── .env             # Configurações editáveis
├── requirements.txt # Dependências Python
├── start_maximus.bat# Arranque automático (Ollama + Maximus)
└── memory/          # Histórico de sessões (criado automaticamente)
    └── 2026-04-16_22-01.json
```

---

## Requisitos

- Windows 10/11
- Python 3.10+
- [Ollama](https://ollama.com) instalado
- Microfone funcional

---

## Instalação

**1. Clona o repositório**
```bash
git clone https://github.com/teu-user/maximus.git
cd maximus
```

**2. Instala as dependências Python**
```bash
python -m pip install -r requirements.txt
```

**3. Instala o Ollama e descarrega o modelo**
```powershell
# Instala Ollama
irm https://ollama.com/install.ps1 | iex

# Descarrega o modelo (~2GB)
ollama pull llama3.2
```

**4. Configura o `.env`**
```ini
THRESHOLD=0.03        # Sensibilidade do microfone (aumenta se não detetar palmas)
CLAP_WINDOW=30        # Segundos para detetar a 2ª palma
MODEL=llama3.2        # Modelo Ollama a usar
OLLAMA_URL=http://localhost:11434/api/chat
SPOTIFY_URI=spotify:track:08mG3Y1vljYA6bvDt4Wqkj
USERNAME=Guide        # O teu nome
MAX_HISTORY=20        # Mensagens de histórico enviadas ao modelo
TIMEOUT=60            # Timeout em segundos para resposta do modelo
```

---

## Como usar

**Arranque automático (recomendado)**

Faz duplo clique em `start_maximus.bat` — arranca o Ollama e o Maximus automaticamente.

**Arranque manual**
```powershell
# Terminal 1 — Ollama
ollama serve

# Terminal 2 — Maximus
python main.py
```

**Modo debug** (para calibrar o microfone)
```powershell
python main.py --debug
```
Mostra o volume captado em tempo real. O `THRESHOLD` no `.env` deve ficar ligeiramente abaixo do pico de uma palma.

---

## Comandos no chat

| Comando      | Ação                                      |
|--------------|-------------------------------------------|
| `!help`      | Lista todos os comandos                   |
| `!spotify`   | Abre o Spotify                            |
| `!instagram` | Abre o Instagram                          |
| `!memoria`   | Lista sessões de memória guardadas        |
| `!limpar`    | Limpa o histórico da sessão atual         |
| `!stats`     | Mostra CPU, RAM e disco                   |
| `!horas`     | Mostra a hora atual                       |
| `sair`       | Encerra o chat e volta a escutar palmas   |

---

## Fluxo de funcionamento

```
Arranque
   │
   ▼
Escuta palmas (microfone ativo)
   │
   ├── 1ª palma detetada
   │       │
   │       ▼
   │   Countdown 30s
   │       │
   │       ├── 2ª palma dentro do tempo
   │       │       │
   │       │       ▼
   │       │   Spotify + Instagram + Chat
   │       │
   │       └── 30s sem 2ª palma
   │               │
   │               ▼
   │           Só Chat
   │
   └── Chat encerrado ("sair")
           │
           ▼
       Volta a escutar palmas
```

---

## Dependências

| Pacote          | Uso                                      |
|-----------------|------------------------------------------|
| `sounddevice`   | Captura de áudio do microfone            |
| `numpy`         | Cálculo de volume RMS                    |
| `rich`          | UI colorida no terminal                  |
| `requests`      | Comunicação com a API do Ollama          |
| `psutil`        | Stats de CPU, RAM e disco                |
| `python-dotenv` | Carregamento do ficheiro `.env`          |
| `pywin32`       | Trazer janela do terminal para frente    |
| `pycaw`         | Controlo de volume do Windows            |
| `comtypes`      | Dependência do pycaw                     |

---

## Calibração do microfone

Se o Maximus não detetar as palmas ou detetar sons aleatórios:

```powershell
python main.py --debug
```

Observa o valor `VOL` em repouso e durante uma palma. Define o `THRESHOLD` no `.env` como um valor entre os dois. Exemplo:
- Ruído de fundo: `0.005`
- Palma: `0.08`
- Threshold ideal: `0.03`

---

## Memória e histórico

Cada sessão de chat é guardada automaticamente em `memory/` com o formato `YYYY-MM-DD_HH-MM.json`. O Maximus carrega automaticamente a sessão mais recente para ter contexto das conversas anteriores.

Para ver as sessões guardadas, usa `!memoria` no chat.

---

## Licença

MIT — usa, modifica e distribui à vontade.
