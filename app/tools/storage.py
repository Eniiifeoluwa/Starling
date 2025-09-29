
from pathlib import Path

def save_artifact(run_id: str, name: str, data: bytes, base_dir='./artifacts'):
    base = Path(base_dir) / run_id
    base.mkdir(parents=True, exist_ok=True)
    path = base / name
    path.write_bytes(data)
    return str(path)
