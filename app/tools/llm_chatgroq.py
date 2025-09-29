
"""ChatGroq wrapper using LangChain Groq integration.

Note: This file expects `GROQ_API_KEY` in the environment.
"""
import os
try:
    from langchain_groq.chat_models import ChatGroq
    from langchain_core.schema import HumanMessage, SystemMessage, AIMessage
except Exception as e:
    # Provide a minimal fallback stub that raises an actionable error when used.
    ChatGroq = None
    HumanMessage = SystemMessage = AIMessage = None

class ChatGroqWrapper:
    def __init__(self, model: str = 'llama-3.1-8b-instant', temperature: float = 0.7):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise RuntimeError('GROQ_API_KEY not set in environment. Please set it before running the Critic agent.')
        if ChatGroq is None:
            raise RuntimeError('langchain_groq is not installed. Install it or use the fallback critic.')
        self.client = ChatGroq(model=model, groq_api_key=api_key, temperature=temperature)

    async def chat(self, messages: list):
        # messages: list of dicts like {'role':'system'|'user', 'content':str}
        converted = []
        for m in messages:
            role = m.get('role')
            content = m.get('content','')
            if role == 'system':
                converted.append(SystemMessage(content=content))
            elif role == 'user':
                converted.append(HumanMessage(content=content))
            else:
                converted.append(HumanMessage(content=content))
        # Use async prediction if available, else sync predict wrapped
        if hasattr(self.client, 'apredict'):
            resp = await self.client.apredict(messages=converted)
            return getattr(resp, 'content', str(resp))
        elif hasattr(self.client, 'predict'):
            resp = self.client.predict(messages=converted)
            return getattr(resp, 'content', str(resp))
        else:
            raise RuntimeError('ChatGroq client has no predict/apredict method.')
