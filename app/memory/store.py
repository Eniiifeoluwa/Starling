
import sqlite3, json
from pathlib import Path

class MemoryStore:
    def __init__(self, path='./memory/db.sqlite'):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self._ensure_tables()

    def _ensure_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS steps (id INTEGER PRIMARY KEY, run_id TEXT, agent TEXT, payload TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS artifacts (id INTEGER PRIMARY KEY, run_id TEXT, name TEXT, path TEXT)''')
        self.conn.commit()

    def save_run_step(self, run_id: str, agent: str, payload: dict):
        c = self.conn.cursor()
        c.execute('INSERT INTO steps (run_id, agent, payload) VALUES (?, ?, ?)', (run_id, agent, json.dumps(payload)))
        self.conn.commit()

    def get_steps(self, run_id: str):
        c = self.conn.cursor()
        c.execute('SELECT agent, payload FROM steps WHERE run_id = ? ORDER BY id', (run_id,))
        return [(a, json.loads(p)) for a,p in c.fetchall()]

    def save_artifact(self, run_id: str, name: str, path: str):
        c = self.conn.cursor()
        c.execute('INSERT INTO artifacts (run_id, name, path) VALUES (?, ?, ?)', (run_id, name, path))
        self.conn.commit()

    def list_artifacts(self):
        c = self.conn.cursor()
        c.execute('SELECT run_id, name, path FROM artifacts ORDER BY id DESC')
        return [{'run_id': r, 'name': n, 'path': p} for r,n,p in c.fetchall()]
