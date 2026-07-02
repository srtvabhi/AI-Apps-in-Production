import streamlit as st
import requests

API_URL = "http://myappdemo123unique.centralindia.azurecontainer.io:8000/ask"

st.title("🤖 My AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask something..."):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    # Build conversation context
    context = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in st.session_state.messages
        ]
    )

    response = requests.post(
        API_URL,
        json={
            "question": f"""
Conversation History:

{context}

Current User Question:
{prompt}
"""
        }
    )

    answer = response.json().get(
        "answer",
        "No response"
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.write(answer)

with st.sidebar:

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
