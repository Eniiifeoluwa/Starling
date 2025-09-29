
"""LangGraph graph definition. Uses real LangGraph if available, else provides a SimpleGraph fallback."""
try:
    from langgraph import Graph, Node, Edge  # type: ignore
    HAS_LANGGRAPH = True
except Exception:
    HAS_LANGGRAPH = False

import asyncio

class SimpleNode:
    def __init__(self, func, name=None):
        self.func = func
        self.name = name or getattr(func, '__name__', 'node')

    async def run(self, ctx):
        return await self.func(ctx)

class SimpleGraph:
    def __init__(self, nodes):
        # nodes: list of (callable, name)
        self.nodes = [SimpleNode(f, name=n) for f,n in nodes]

    async def run_async(self, ctx):
        for n in self.nodes:
            ctx = await n.run(ctx)
        return ctx

    def run_sync(self, ctx):
        return asyncio.run(self.run_async(ctx))

def build_graph(nodes):
    """nodes: list of tuples (callable, name)"""
    if HAS_LANGGRAPH:
        # User-installed LangGraph: build using its API.
        # This is a conceptual mapping; depending on LangGraph version this block may need adjustments.
        g = Graph(name='starling_graph')
        # create nodes and edges linearly
        lg_nodes = []
        for func, name in nodes:
            # LangGraph Node wrapper is implementation-specific;
            # here we assume a simple Node factory exists where Node(func) works.
            lg_nodes.append(Node(func, name=name))
            g.add_node(lg_nodes[-1])
        # chain edges
        for i in range(len(lg_nodes)-1):
            g.add_edge(Edge(lg_nodes[i], lg_nodes[i+1]))
        return g
    else:
        return SimpleGraph(nodes)
