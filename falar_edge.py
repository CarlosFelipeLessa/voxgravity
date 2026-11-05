import sys
from pathlib import Path

SRC_PATH = Path(__file__).resolve().parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from voxgravity.tts import falar

def main():
    if len(sys.argv) < 2:
        print("Uso: python falar_edge.py \"Texto\" [cristina|antonio|francisca]")
        return
    text = sys.argv[1]
    choice = sys.argv[2].lower() if len(sys.argv) > 2 else "cristina"
    falar(text, choice)

if __name__ == "__main__":
    main()
