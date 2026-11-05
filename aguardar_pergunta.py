import sys
from pathlib import Path

# Adiciona o diretório src ao path para resolução de módulos
SRC_PATH = Path(__file__).resolve().parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from voxgravity.bridge import FileBridge

def main():
    print("Iniciando escuta por nova pergunta via FileBridge...", flush=True)
    # Limpa pergunta pendente antiga antes de iniciar a escuta
    FileBridge.limpar_pergunta()
    
    pergunta = FileBridge.aguardar_pergunta(timeout=7200, intervalo=0.2)
    if pergunta:
        print(f"[PERGUNTA_RECEBIDA]: {pergunta}")
        sys.exit(0)
    else:
        print("Timeout de espera.")
        sys.exit(0)

if __name__ == "__main__":
    main()
