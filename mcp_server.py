import os
import sys
from pathlib import Path

SRC_PATH = Path(__file__).resolve().parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from mcp.server.mcpserver import MCPServer
from voxgravity.config import CONFIG
from voxgravity.tts import falar as tts_falar

server = MCPServer("VoxGravity")

@server.tool()
def falar(texto: str, voz: str = "cristina") -> str:
    """
    Sintetiza e reproduz em voz alta uma mensagem amigável para o usuário.
    
    Opções recomendadas para 'voz':
    - 'cristina': Feminino dinâmico, jovem e expressivo (calibrado).
    - 'antonio': Masculino encorpado, calmo e companheiro de trabalho (calibrado).
    - 'francisca': Feminino neutro clássico.
    """
    voz_key = voz.lower().strip()
    sucesso = tts_falar(texto, voz=voz_key, block=False)
    if sucesso:
        return f"Áudio falado com sucesso [Voz: {voz_key}]: \"{texto}\""
    return f"Erro ao sintetizar áudio para o texto solicitado."

@server.tool()
def listar_vozes() -> str:
    """Lista as vozes disponíveis e seus ajustes de tom calibrados."""
    presets = CONFIG.get("tts", {}).get("presets", {})
    res = ["Vozes de estúdio disponíveis no VoxGravity:"]
    for nome, cfg in presets.items():
        desc = cfg.get("description", "Voz neural de estúdio")
        res.append(f"- '{nome}': {desc}")
    return "\n".join(res)

if __name__ == "__main__":
    server.run("stdio")
