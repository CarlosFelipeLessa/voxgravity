import json
import os
from pathlib import Path

# Raiz do projeto baseada na localização deste arquivo
PACKAGE_DIR = Path(__file__).resolve().parent
SRC_DIR = PACKAGE_DIR.parent
ROOT_DIR = SRC_DIR.parent

CONFIG_FILE = ROOT_DIR / "config.json"

DEFAULT_CONFIG = {
    "hotkey": "shift+'",
    "debounce_seconds": 0.35,
    "audio": {
        "sample_rate": 16000,
        "channels": 1,
        "language": "pt-BR"
    },
    "beeps": {
        "start_freq": 1200,
        "stop_freq": 850,
        "sent_freq": 1400,
        "error_freq": 450
    },
    "tts": {
        "default_voice": "cristina",
        "presets": {
            "cristina": {
                "voice": "pt-BR-ThalitaMultilingualNeural",
                "pitch": "+8Hz",
                "rate": "+5%",
                "description": "Feminino jovem, dinâmico e expressivo"
            },
            "antonio": {
                "voice": "pt-BR-AntonioNeural",
                "pitch": "-8Hz",
                "rate": "-5%",
                "description": "Masculino encorpado e calmo"
            },
            "francisca": {
                "voice": "pt-BR-FranciscaNeural",
                "pitch": "+0Hz",
                "rate": "+0%",
                "description": "Feminino neutro clássico"
            }
        }
    },
    "bridge": {
        "folder": "bridge",
        "pergunta_file": "pergunta.txt",
        "resposta_file": "resposta.txt",
        "acao_file": "acao.json"
    }
}

def load_config() -> dict:
    """Carrega as configurações do config.json com fallback seguro."""
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            # Mescla de 1 nível com fallbacks
            config = DEFAULT_CONFIG.copy()
            config.update(user_config)
            return config
    except Exception:
        return DEFAULT_CONFIG

CONFIG = load_config()

# Diretórios e caminhos do Bridge
BRIDGE_DIR = ROOT_DIR / CONFIG.get("bridge", {}).get("folder", "bridge")
PERGUNTA_FILE = BRIDGE_DIR / CONFIG.get("bridge", {}).get("pergunta_file", "pergunta.txt")
RESPOSTA_FILE = BRIDGE_DIR / CONFIG.get("bridge", {}).get("resposta_file", "resposta.txt")
ACAO_FILE = BRIDGE_DIR / CONFIG.get("bridge", {}).get("acao_file", "acao.json")

# Garante a existência da pasta bridge
BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
