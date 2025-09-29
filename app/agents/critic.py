
"""Critic node: uses ChatGroq to provide a structured critique of the idea."""
from app.tools.llm_chatgroq import ChatGroqWrapper
from app.memory.store import MemoryStore

mem = MemoryStore('./memory/db.sqlite')
llm = ChatGroqWrapper()

async def critic_node_func(ctx: dict):
    idea = ctx.get('idea','')
    sources = ctx.get('sources', [])
    system = "You are a concise startup evaluator. Return JSON with keys: novelty (0-1), market_fit (0-1), risks (list), suggestions (list)."
    user = f"Idea: {idea}\nSources: {sources[:3]}\nRespond in strict JSON only."
    messages = [{'role':'system','content':system}, {'role':'user','content':user}]
    try:
        resp = await llm.chat(messages)
    except Exception as e:
        # fallback heuristic if LLM fails
        resp = '{"novelty":0.5, "market_fit":0.6, "risks":[], "suggestions":["Use niche targeting"]}'
    # save as text and try parse
    mem.save_run_step(ctx['run_id'], 'critic', {'raw': resp})
    try:
        import json
        parsed = json.loads(resp)
    except Exception:
        parsed = {'novelty':0.5, 'market_fit':0.6, 'risks':[], 'suggestions':[]}
    ctx['critique'] = parsed
    return ctx
