# app/main.py
import streamlit as st
from app.orchestrator import GraphOrchestrator

def run():
    st.set_page_config(page_title='Starling Agent', layout='wide')
    st.title('Starling Agent 🐦 — Autonomous Startup Builder (LangGraph + ChatGroq)')

    st.markdown('Enter a startup idea, choose dry-run or real-run, and watch the agents work together. No OpenAI used — ChatGroq is the LLM.')

    idea = st.text_area('Startup idea', value='A smart email assistant for developers', height=140)
    cols = st.columns([3,1])
    with cols[0]:
        dry_run = st.checkbox('Dry run (no external actions)', value=True)
        start = st.button('Start Run')
    with cols[1]:
        st.markdown('**Actions**')
        if st.button('Refresh'):
            st.experimental_rerun()

    orch = GraphOrchestrator()

    if start and idea.strip():
        run_id = orch.start_run(idea.strip(), dry_run=dry_run)
        st.success(f'Run started: {run_id}')

    st.header('Recent runs')
    runs = orch.list_recent_runs(limit=20)
    if not runs:
        st.info('No runs yet — start one above.')
    for r in runs:
        with st.expander(f"Run {r['run_id']} — status: {r.get('status','unknown')}"):
            st.json(r.get('ctx', {}))
            steps = orch.get_run_steps(r['run_id'])
            if steps:
                st.subheader('Steps (agent -> payload)')
                for agent, payload in steps:
                    st.write(f"**{agent}**")
                    st.write(payload)
            artifacts = [a for a in orch.list_artifacts() if a['run_id']==r['run_id']]
            if artifacts:
                st.subheader('Artifacts')
                for a in artifacts:
                    st.write(a)
                    if 'path' in a:
                        try:
                            with open(a['path'],'rb') as f:
                                st.download_button(label=f"Download {a['name']}", data=f, file_name=a['name'])
                        except Exception as e:
                            st.write('Error preparing download:', e)
