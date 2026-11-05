import os
import sys
import time
from pathlib import Path
from typing import Optional
from voxgravity.config import BRIDGE_DIR, PERGUNTA_FILE, RESPOSTA_FILE

class FileBridge:
    """Gerencia a comunicação assíncrona por arquivos entre o usuário e o Agente Antigravity."""
    
    @staticmethod
    def limpar_pergunta() -> None:
        """Remove pergunta pendente anterior."""
        try:
            if PERGUNTA_FILE.exists():
                PERGUNTA_FILE.unlink(missing_ok=True)
        except Exception:
            pass

    @staticmethod
    def enviar_pergunta(texto: str) -> bool:
        """Escreve a transcrição da pergunta para que o agente processe."""
        texto = texto.strip()
        if not texto:
            return False
        try:
            with open(PERGUNTA_FILE, "w", encoding="utf-8") as f:
                f.write(texto)
            return True
        except Exception as e:
            print(f"[Bridge] Erro ao enviar pergunta: {e}")
            return False

    @staticmethod
    def ler_pergunta(remover: bool = True) -> Optional[str]:
        """Lê a pergunta pendente no arquivo se existir."""
        if not PERGUNTA_FILE.exists():
            return None
        try:
            with open(PERGUNTA_FILE, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
            if remover and conteudo:
                PERGUNTA_FILE.unlink(missing_ok=True)
            return conteudo if conteudo else None
        except Exception:
            return None

    @staticmethod
    def enviar_resposta(texto: str) -> bool:
        """Escreve a resposta do agente para a interface/áudio."""
        texto = texto.strip()
        if not texto:
            return False
        try:
            with open(RESPOSTA_FILE, "w", encoding="utf-8") as f:
                f.write(texto)
            return True
        except Exception as e:
            print(f"[Bridge] Erro ao enviar resposta: {e}")
            return False

    @staticmethod
    def ler_resposta() -> Optional[str]:
        """Lê a resposta do agente se disponível."""
        if not RESPOSTA_FILE.exists():
            return None
        try:
            with open(RESPOSTA_FILE, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
            return conteudo if conteudo else None
        except Exception:
            return None

    @staticmethod
    def aguardar_pergunta(timeout: float = 7200, intervalo: float = 0.2) -> Optional[str]:
        """Bloqueia até que uma pergunta seja gravada ou o timeout expire."""
        inicio = time.time()
        while time.time() - inicio < timeout:
            if PERGUNTA_FILE.exists():
                time.sleep(0.1)
                conteudo = FileBridge.ler_pergunta(remover=True)
                if conteudo:
                    return conteudo
            time.sleep(intervalo)
        return None
