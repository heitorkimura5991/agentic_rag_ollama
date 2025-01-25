import ollama
from typing import Literal, List, Dict

from langchain_ollama import ChatOllama

from prompts import default_prompt

def call_llm(context: str, prompt: str, system_prompt: str = default_prompt, output_format: Literal["", "json"] = "", chat_memory: List[Dict[str, str]] = []):
    response = ollama.chat(
        model="llama3.2:latest",
        stream=True,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"Context: {context}, Question: {prompt}"
            }
        ] + [],
        format=output_format)
    for chunk in response:
        if chunk["done"] is False:
            yield chunk["message"]["content"]
        else:
            break

def get_llm(model: Literal['llama3.2:latest', 'llama3.2:1b'], temperature: float, max_tokens: int = 500):
    llm = ChatOllama(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return llm