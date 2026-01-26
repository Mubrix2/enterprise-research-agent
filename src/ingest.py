import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import FakeEmbeddings #We'll swap this for GitHub Models later
from langchain_chroma import Chroma
from src.config import settings

def run_ingestion():
    # 1. Load Documents
    print(f"--- Loading PDFs from {settings.data_dir} ---")
    loader = DirectoryLoader(str(settings.data_dir), glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    if not documents:
        print("No PDFs found! Add some files to the /data folder.")
        return

    # 2. Split Text (Chunking)
    # AI models have "context limits." We break big docs into 1000-character pieces.
    print("--- Splitting documents into chunks ---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    # 3. Create Vector Store (ChromaDB)
    # This turns text into math and saves it to the /chroma_db folder.
    print(f"--- Saving to Vector DB at {settings.db_dir} ---")
    # For now, we use a simple embedding. In the next step, we'll use actual AI embeddings.
    embeddings = FakeEmbeddings(size=1536) 
    
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(settings.db_dir)
    )
    
    print("--- Ingestion Complete! ---")

if __name__ == "__main__":
    run_ingestion()