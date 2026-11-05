import streamlit as st
import ollama
from ddgs import DDGS

st.set_page_config(
    page_title="Mindmate",
    page_icon="🎓"
)

# Simple UI
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 35px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🎓 Mindmate</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask me any education-related question! 💬</div>',
    unsafe_allow_html=True
)

# Store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Student question
question = st.chat_input("Ask your question...")

if question:

    st.chat_message("user").write(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Search the web
    search_results = list(
        DDGS().text(
            question,
            max_results=5
        )
    )

    sources = ""

    for result in search_results:
        sources += f"""
Title: {result.get('title', '')}
Source: {result.get('href', '')}
Information: {result.get('body', '')}

"""

    # AI instruction
    prompt = f"""
You are an AI Education Assistant.

Give clear and simple answers to students.

Use the web search information below.
Do not invent sources.

Student question:
{question}

Web search information:
{sources}

Give a clear answer and explanation.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    with st.chat_message("assistant"):
        st.write(answer)

        if search_results:
            st.markdown("### 🔎 Sources")

            for result in search_results:
                title = result.get("title", "Source")
                url = result.get("href", "")

                if url:
                    st.markdown(f"- [{title}]({url})")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })