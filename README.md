# Agentic RAG with Ollama
An example of RAG and agentic workflows using local AI models through Ollama.

## Project Structure and Overview
The title of this project is composed of three main parts:
1. "Agentic": stands for the use of multiple AI agents to elaborate a more complete analysis of given documents (websites, PDFs, etc.) and give assertive answers to the user **(work in progress)**.
2. RAG: the process of Retrieved Augmented Generation (RAG) is composed of data processing pipelines to retrieve information from many different sources, such as websites, PDFs, spreadsheets and other file types. This step serves as a "prompt enhancing method" towards what the AI agents will be given to generate answers or actions.
3. Ollama: it is an AI framework (not really sure if is properly called like this) for Python that speeds up AI Language Models instantiation and usage, besides making them available in a "friendly" format for normal humans.

As for the project structure, there are 4 main modules that feeds the application.
### Documents (docs.py)
Deals with file processing, text splitting, etc.
### LLMs (llms.py)
Deals with AI model configuration and instantiation.
### Scrapers (scrapers.py)
Deals with website scraping (information extraction).
### Vector Database Setup (vector_db.py)
Deals with vector database management.
___
## Usage
1. Clone this repository using git
```
git clone https://github.com/heitorkimura5991/agentic_rag_ollama.git
```
2. Create virtual environment (I'm using conda)
```
conda create --name <name_of_env> --file requirements.txt
```
3. Run
```
streamlit run app.py
```
___
## Next Steps
- Create Agents
- Test for large PDF files
- Expand to other vector database libraries
- Generate files with data analysis