
# Starling Agent — LangGraph + Streamlit + ChatGroq

Starling Agent is an autonomous, agentic scaffold that uses **LangGraph** (with a safe fallback),
**Streamlit** for the UI, and **ChatGroq** (via LangChain Groq integration) as the LLM for reasoning.
This repo is intentionally built **without OpenAI** usage.

## Quickstart (local)
1. Create a virtualenv and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Groq API key as an environment variable:
   ```bash
   export GROQ_API_KEY="your_groq_api_key"
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app/main.py
   ```

## What it does
- Accepts a startup idea in the UI.
- Runs a LangGraph-managed agent pipeline (Reader → Critic → Builder).
- Uses ChatGroq for critique and generation tasks.
- Stores run steps and artifacts in `./memory/db.sqlite`.
- Supports a LangGraph installation if available, otherwise uses a bundled fallback engine so the app runs out-of-the-box.

## Important safety note
The `CodeExecutor` included is a simple executor intended for local, trusted use only. **Do not** run untrusted code with it.

## Structure
See the repository for file-by-file structure. If you'd like, I can add GitHub push support, SerpAPI integration, or a deployer node next.
