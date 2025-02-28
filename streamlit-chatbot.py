from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
import json
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage

load_dotenv()

model = os.getenv('LLM_MODEL', 'gpt-4o')

def main():
    st.title("Streamlit Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=f"The current date is: {datetime.now().date()}")
        ]

    for message in st.session_state.messages:
        message_json = json.loads(message.json())
        with st.chat_message(message_json["type"]):
            st.markdown(message_json["content"])        

    if prompt := st.chat_input("What would you like to do today?"):
        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append(HumanMessage(content=prompt))

        with st.chat_message("assistant"):
            chatbot = ChatOpenAI(model=model)
            stream = chatbot.stream(st.session_state.messages)
            response = st.write_stream(stream)

        st.session_state.messages.append(AIMessage(content=response))


if __name__ == "__main__":
    main()