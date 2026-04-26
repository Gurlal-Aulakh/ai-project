import streamlit as st
from app.agent_runner import run_ai_assistant_sync

st.set_page_config(
    page_title="AI Project Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Project Assistant")
st.caption("Main Agent + Worker Agents + MCP + Memory + RAG + Graph DB + Semantic Cache")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "debug_history" not in st.session_state:
    st.session_state.debug_history = []

with st.sidebar:
    st.header("System Status")
    st.write("✅ Main Agent")
    st.write("✅ Worker Agents")
    st.write("✅ MCP Tools")
    st.write("✅ Long-Term Memory")
    st.write("✅ Hybrid Retrieval")
    st.write("✅ Graph DB")
    st.write("✅ Semantic Cache")

    show_debug = st.checkbox("Show debug details", value=True)

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.debug_history = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask something about your AI project...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = run_ai_assistant_sync(user_input)

        answer = result["answer"]
        st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.session_state.debug_history.append(result)

if show_debug and st.session_state.debug_history:
    st.divider()
    st.subheader("Debug Panel")

    latest = st.session_state.debug_history[-1]

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Cache Status:**")
        st.code(latest.get("cache_status", ""))

    with col2:
        st.write("**Tools Used:**")
        st.code(latest.get("tools_used", []))

    with st.expander("Full Debug Result"):
        st.text(latest.get("debug", ""))