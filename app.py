import sys
from pathlib import Path

# Ensure repo root is in sys.path
sys.path.append(str(Path(__file__).parent))

from app.main import run

if __name__ == "__main__":
    run()
