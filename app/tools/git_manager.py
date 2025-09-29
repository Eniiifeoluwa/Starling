
from pathlib import Path
from git import Repo

class GitManager:
    def __init__(self, base_dir: str = './repos'):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def init_repo(self, name: str, files: dict):
        repo_path = self.base_dir / name
        repo_path.mkdir(parents=True, exist_ok=True)
        for fname, content in files.items():
            p = repo_path / fname
            p.write_text(content, encoding='utf-8')
        repo = Repo.init(repo_path)
        repo.index.add([str(p.relative_to(repo_path)) for p in repo_path.rglob('*')])
        repo.index.commit('Initial commit from Starling Agent')
        return str(repo_path)
