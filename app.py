import os

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from tools import tools


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="LangChain AI Agent",
    page_icon="🤖",
    layout="centered"
)


# ==========================================
# TITLE
# ==========================================

st.title("🤖 LangChain Conversational Agent")

st.caption(
    "A conversational AI agent powered by LangChain + Groq"
)


# ==========================================
# API KEY CHECK
# ==========================================

if not GROQ_API_KEY:

    st.error(
        "GROQ_API_KEY not found in .env file."
    )

    st.stop()


# ==========================================
# CREATE LLM
# ==========================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY,
)


# ==========================================
# CREATE AGENT
# ==========================================

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are a helpful conversational AI research assistant.

You have access to these tools:

1. Calculator
2. Web Research
3. Text Summarizer
4. Word Counter
5. Current Date and Time

Use tools whenever they are appropriate.

Calculator:
Use for mathematical calculations.

Web Research:
Use when the user asks for factual research about a topic.

Text Summarizer:
Use when the user provides text and asks for a summary.

Word Counter:
Use when the user asks how many words are in a text.

Current Date and Time:
Use for current date and time questions.

Remember the conversation context and answer naturally.

Do not mention internal reasoning.
Give clear and useful answers.
Do not use LaTeX or math markup. Write numbers and equations in plain text, like 25 * 48 / 5 = 240.
"""
)


# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("🛠️ Available Tools")

    st.write("🧮 Calculator")
    st.write("🌐 Web Research")
    st.write("📝 Text Summarizer")
    st.write("🔢 Word Counter")
    st.write("🕐 Date & Time")

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ==========================================
# DISPLAY PREVIOUS MESSAGES
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# CHAT INPUT
# ==========================================

user_input = st.chat_input(
    "Ask your LangChain agent..."
)


# ==========================================
# PROCESS USER MESSAGE
# ==========================================

if user_input:

    # Display user message
    with st.chat_message("user"):

        st.markdown(user_input)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # ======================================
    # PREPARE CONVERSATION FOR AGENT
    # ======================================

    conversation = []

    for message in st.session_state.messages:

        conversation.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )


    # ======================================
    # RUN AGENT
    # ======================================

    with st.chat_message("assistant"):

        with st.spinner("🤔 Agent is thinking..."):

            try:

                result = agent.invoke(
                    {
                        "messages": conversation
                    }
                )

                final_message = result["messages"][-1]

                answer = final_message.content

                st.markdown(answer)


                # ==================================
                # SAVE ASSISTANT MESSAGE
                # ==================================

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )