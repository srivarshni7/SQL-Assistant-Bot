import streamlit as st
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# -------------------------
# Load Environment Variables
# -------------------------
load_dotenv()

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="SQL Assistant Pro",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
}
.subtitle {
    text-align:center;
    color:gray;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.markdown(
    "<div class='main-title'>🤖 SQL Assistant Pro</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Generate SQL Queries Using AI</div>",
    unsafe_allow_html=True
)

# -------------------------
# API Key
# -------------------------
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()

# -------------------------
# Session State
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:

    st.title("⚙️ Settings")

    db_type = st.selectbox(
        "Database",
        [
            "MySQL",
            "PostgreSQL",
            "SQLite",
            "SQL Server"
        ]
    )

    st.metric(
        "Queries Generated",
        st.session_state.query_count
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("💡 Example Questions")

    st.write("""
    • Show all employees

    • Top 5 highest salaries

    • Customers from Chennai

    • Orders in last 30 days

    • Total sales by month
    """)

# -------------------------
# Display Chat History
# -------------------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if msg["role"] == "assistant":

            st.markdown(msg["content"])

        else:

            st.write(msg["content"])

# -------------------------
# User Input
# -------------------------
question = st.chat_input(
    "Ask your SQL question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    prompt = f"""
You are an expert SQL developer.

Generate SQL query in {db_type}.

Return output in this format:

SQL:
<query>

Explanation:
<simple explanation>

User Request:
{question}
"""

    with st.spinner("Generating SQL..."):

        response = llm.invoke(prompt)

        answer = response.content.strip()

    st.session_state.query_count += 1

    with st.chat_message("assistant"):

        st.markdown(answer)

        st.download_button(
            label="⬇ Download SQL",
            data=answer,
            file_name="query.sql",
            mime="text/plain"
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )