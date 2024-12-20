import streamlit as st

from docs import process_document
from llms import call_llm
from scrapers import scrape_urls
from vector_db import add_to_vector_collection, query_collection, re_rank_cross_encoders


def main() -> None:
    with st.sidebar:
        st.set_page_config(page_title="Docs")
        uploaded_file = st.file_uploader(
            "**Carregue arquivos em PDF**", type=["pdf"], accept_multiple_files=False
        )

        urls = st.text_input("**Insira URLs que deseja consultar**")
        urls = urls.split(",")

        process = st.button("Carregar")

        if uploaded_file and process:
            normalize_uploaded_file_name = uploaded_file.name.translate(
                str.maketrans({"-": "_", ".": "_", " ": "_"})
            )

            all_splits = process_document(uploaded_file)
            add_to_vector_collection(all_splits, normalize_uploaded_file_name)
            st.success("Dados adicionados ao banco!")

        elif urls and process:
            url_splits = scrape_urls(urls)
            add_to_vector_collection(url_splits, "url_1")
            st.success("Dados adicionados ao banco!")

    st.header("AI Assistant")
    prompt = st.text_area("**Pergunte sobre o documento**")
    ask = st.button("Enviar")

    if ask and prompt:
        with st.spinner("Pensando..."):    
            results = query_collection(prompt)
            context = results.get("documents")[0]
            relevant_text, relevant_text_ids = re_rank_cross_encoders(prompt, context)
        
            response = call_llm(context=relevant_text, prompt=prompt)
            st.write_stream(response)

        with st.expander("Ver documentos utilizados"):
            st.write(results["documents"])

        with st.expander("Ver document_ids mais relevantes"):
            st.write(relevant_text_ids)
            st.write(relevant_text)


if __name__ == "__main__":
    main()
