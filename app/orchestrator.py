
import uuid, asyncio
from app.langgraph_def import build_graph
from app.memory.store import MemoryStore
from app.agents.reader import reader_node_func
from app.agents.critic import critic_node_func
from app.agents.builder import builder_node_func

class GraphOrchestrator:
    def __init__(self):
        self.memory = MemoryStore('./memory/db.sqlite')
        nodes = [(reader_node_func, 'reader'), (critic_node_func, 'critic'), (builder_node_func, 'builder')]
        self.graph = build_graph(nodes)
        self.runs = {}

    def start_run(self, idea: str, dry_run: bool = True):
        run_id = str(uuid.uuid4())
        ctx = {'idea': idea, 'dry_run': dry_run, 'run_id': run_id}
        self.memory.save_run_step(run_id, 'orchestrator', {'started': True})
        # schedule execution
        if hasattr(self.graph, 'run_async'):
            # run in background asyncio task
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = None
            if loop and loop.is_running():
                asyncio.create_task(self._run_async(run_id, ctx))
            else:
                # start a background thread if no running loop
                import threading
                t = threading.Thread(target=self._run_sync, args=(run_id, ctx), daemon=True)
                t.start()
        else:
            # fallback sync run
            self._run_sync(run_id, ctx)
        self.runs[run_id] = {'run_id': run_id, 'status': 'running', 'ctx': ctx}
        return run_id

    async def _run_async(self, run_id, ctx):
        try:
            res = await self.graph.run_async(ctx)
        except Exception as e:
            res = {'error': str(e)}
        self.memory.save_run_step(run_id, 'graph_complete', res)
        self.runs[run_id]['status'] = 'completed'
        self.runs[run_id]['ctx'] = res

    def _run_sync(self, run_id, ctx):
        try:
            if hasattr(self.graph, 'run_sync'):
                res = self.graph.run_sync(ctx)
            else:
                import asyncio
                res = asyncio.run(self.graph.run_async(ctx))
        except Exception as e:
            res = {'error': str(e)}
        self.memory.save_run_step(run_id, 'graph_complete', res)
        self.runs[run_id]['status'] = 'completed'
        self.runs[run_id]['ctx'] = res

    def list_recent_runs(self, limit=20):
        return list(self.runs.values())[-limit:]

    def get_run_steps(self, run_id):
        return self.memory.get_steps(run_id)

    def list_artifacts(self):
        return self.memory.list_artifacts()
