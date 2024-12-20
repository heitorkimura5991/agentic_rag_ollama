from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


def scrape_urls(urls: list[str]):
    loader = AsyncChromiumLoader(urls=urls, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    html = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["h2", "p"])
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        separators=["\n\n", ".", "?", "!", " ", ""]
    )

    return text_splitter.split_documents(docs_transformed)

# print(scrape_urls(['https://saudepets.com.br/10-razoes-irresistiveis-para-escolher-o-melhor-plano-de-saude-para-gatos-em-2024/']))