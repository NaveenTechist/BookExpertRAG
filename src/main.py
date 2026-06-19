import streamlit as st
import subprocess
import sys
import importlib
import query

importlib.reload(query)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Book Expert QA Bot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

print("MAIN FILE STARTED")

st.markdown("""
<style>

/* Main Background */
.stApp{
    background-color:#0F1117;
    color:#F8FAFC;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #2D3748;
}

/* Typography */
h1,h2,h3,h4,h5,h6{
    color:#F8FAFC;
}

/* Sidebar Buttons */
.stSidebar .stButton button{
    width:100%;
    background:#1E293B;
    color:#F8FAFC;
    border:1px solid #2D3748;
    border-radius:12px;
    height:48px;
    margin-bottom:8px;
}

.stSidebar .stButton button:hover{
    border:1px solid #10A37F;
}

/* Chat Messages */
[data-testid="stChatMessage"]{
    border-radius:16px;
    padding:12px;
}

/* User */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){
    background:#1E293B;
}

/* Assistant */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]){
    background:#161B22;
}

/* Chat Input */
.stChatInputContainer{
    background:#0F1117 !important;
}

/* Success Box */
.success-card{
    background:#1E293B;
    border:1px solid #22C55E;
    border-radius:12px;
    padding:12px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("# Book Expert QA Bot ")

    st.caption("RAG Powered Document Assistant")

    st.divider()

    if st.button("Ingest Documents"):

        try:
            with st.spinner("Creating embeddings..."):

                subprocess.run(
                    [sys.executable, "ingest.py"],
                    check=True
                )

            st.success("Documents indexed successfully!")

        except Exception as e:
            st.error(str(e))

    st.divider()

    st.caption("Version 1.0.0")

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("AI Document Q&A")

st.caption(
    "Ask questions about your PDFs and documents using Retrieval-Augmented Generation."
)

st.divider()

# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# --------------------------------------------------
# FIXED CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask about your documents..."
)

if question:

    st.session_state.messages.append({
        "role":"user",
        "content":question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching documents..."):

            try:

                answer = query.ask_question(question)

            except Exception as e:

                answer = f"Error: {str(e)}"

        st.markdown(answer)

    st.session_state.messages.append({
        "role":"assistant",
        "content":answer
    })

    st.rerun()