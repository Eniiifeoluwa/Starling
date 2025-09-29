
import asyncio
from app.tools.web_search import WebSearch

def test_web_search():
    s = WebSearch()
    res = asyncio.run(s.search('hello', limit=2))
    assert isinstance(res, list) and len(res) == 2
