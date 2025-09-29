
"""Simple code executor — UNSAFE. For trusted local testing only."""
import asyncio, tempfile
from pathlib import Path

class CodeExecutor:
    def __init__(self, sandbox_dir: str = '.sandboxes'):
        self.sandbox_dir = Path(sandbox_dir)
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)

    async def run_python(self, code: str, timeout: int = 5):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            path = f.name
        proc = await asyncio.create_subprocess_exec('python', path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
            return {'timeout': True, 'stdout': '', 'stderr': 'Timed out'}
        return {'stdout': out.decode(), 'stderr': err.decode(), 'timeout': False}
