import sys
from pathlib import Path

SRC_PATH = Path(__file__).resolve().parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from voxgravity.ui import main as ui_main
from voxgravity.cli import main as cli_main

def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["--cli", "-c", "cli"]:
        cli_main()
    else:
        ui_main()

if __name__ == "__main__":
    main()
