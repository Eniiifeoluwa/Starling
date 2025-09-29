
"""Reader node: performs lightweight web search (mock or real) and stores sources in context."""
from app.tools.web_search import WebSearch
from app.memory.store import MemoryStore

search = WebSearch()
mem = MemoryStore('./memory/db.sqlite')

async def reader_node_func(ctx: dict):
    idea = ctx.get('idea','')
    results = await search.search(idea, limit=5)
    ctx['sources'] = results
    mem.save_run_step(ctx['run_id'], 'reader', {'found': len(results), 'examples': results[:2]})
    return ctx
