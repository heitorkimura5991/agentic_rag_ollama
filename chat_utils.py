import json
from pathlib import Path

from langchain.schema import messages_from_dict, messages_to_dict
from langchain_community.chat_message_histories.file import FileChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory.buffer import ConversationBufferMemory


class SafeFileChatMessageHistory(FileChatMessageHistory):
    @property
    def messages(self):
        file_path = Path(self.file_path)
        if not file_path.exists() or file_path.stat().st_size == 0:
            file_path.write_text('[]', encoding=self.encoding)
            return []
        try:
            items = json.loads(file_path.read_text(encoding=self.encoding))
            messages = messages_from_dict(items)
            return messages
        except json.JSONDecodeError:
            return []

    def add_message(self, message):
        messages = messages_to_dict(self.messages)
        messages.append(messages_to_dict([message])[0])
        self.file_path.write_text(
            json.dumps(messages, ensure_ascii=self.ensure_ascii), encoding=self.encoding
        )

def get_chat_prompt_template():
    return ChatPromptTemplate(
        input_variables=["content", "messages"],
        messages=[
            SystemMessagePromptTemplate.from_template(
                """
                    Você é um assistente muito educado que auxilia no atendimento de vários serviços.
                """
            ),
            MessagesPlaceholder(variable_name="messages"),
            HumanMessagePromptTemplate.from_template("{content}"),
        ],
    )

def get_memory():
    return ConversationBufferMemory(
        memory_key="messages",
        chat_memory=SafeFileChatMessageHistory(file_path="memory.json"),
        return_messages=True,
        input_key="content",
    )