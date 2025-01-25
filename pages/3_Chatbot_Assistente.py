from typing import Literal
import streamlit as st
from dotenv import load_dotenv
import os

from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory

from langchain_ollama import ChatOllama

load_dotenv()
def get_llm(model: Literal['llama3.2:latest', 'llama3.2:1b'], temperature: float, max_tokens: int = 500):
    llm = ChatOllama(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return llm

llm = get_llm(model='llama3.2:latest', temperature=0.1)

human_template = f"{{question}}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", human_template)
    ]
)

chain = prompt_template | llm

def get_redis_history(session_id: str) -> BaseChatMessageHistory:
    return RedisChatMessageHistory(session_id=session_id, url = f"redis://:{os.getenv('REDIS_PASSWORD')}@localhost:6379/0")

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_redis_history,
    input_messages_key="question",
    history_messages_key="history"
)

while True:
    user_question = input(">>>>")
    result = chain_with_history.invoke(
        {"question": user_question},
        config = {"configurable": {"session_id":"test_1"}},
    )
    print(result.content)