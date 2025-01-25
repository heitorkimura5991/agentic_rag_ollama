import streamlit as st

from llms import call_llm
from prompts import schedule_prompt


def main() -> None:

    st.title("Ferramenta de Agendamento via IA")
    prompt = st.text_area("**Digite sua instrução**")
    ask = st.button("Enviar")    

    if ask and prompt:
        with st.spinner("Pensando..."):
            response = call_llm(context="Você é um assistente de agendamentos.", prompt=prompt, system_prompt=schedule_prompt, output_format='json')
            st.write_stream(response)

if __name__ == "__main__":
    main()