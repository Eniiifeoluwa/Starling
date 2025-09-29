
"""Mockable web search tool. Replace with SerpAPI/Bing adapters for production."""
import asyncio

class WebSearch:
    def __init__(self):
        pass

    async def search(self, query: str, limit: int = 5):
        await asyncio.sleep(0.05)
        return [{'title': f'Mock result {i+1} for {query}', 'url': f'https://example.com/{i}'} for i in range(limit)]
