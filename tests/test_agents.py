
import asyncio
from app.agents.reader import reader_node_func
from app.agents.critic import critic_node_func
from app.agents.builder import builder_node_func

def test_reader_builder_flow():
    ctx = {'idea':'fast grocery delivery', 'dry_run':True, 'run_id':'test-run'}
    res = asyncio.run(reader_node_func(ctx.copy()))
    assert 'sources' in res

def test_full_pipeline():
    ctx = {'idea':'smart scheduler', 'dry_run':True, 'run_id':'test-run-2'}
    ctx = asyncio.run(reader_node_func(ctx))
    ctx = asyncio.run(critic_node_func(ctx))
    ctx = asyncio.run(builder_node_func(ctx))
    assert 'critique' in ctx and 'artifacts' in ctx
