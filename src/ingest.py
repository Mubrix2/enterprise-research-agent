import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from src/
sys.path.insert(0, project_root)

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import FakeEmbeddings
from langchain_chroma import Chroma
from src.config import settings
import shutil

def clear_vector_db():
    """Clear the existing vector database."""
    if os.path.exists(settings.db_dir):
        shutil.rmtree(settings.db_dir)
        print(f"Cleared existing vector database at {settings.db_dir}")

def run_ingestion():
    """
    Main ingestion pipeline:
    1. Load PDF documents from data directory
    2. Split into chunks
    3. Create embeddings and store in vector database
    """
    print("=" * 60)
    print("Starting Document Ingestion Pipeline")
    print("=" * 60)
    
    # Clear existing database to avoid duplicates
    clear_vector_db()
    
    # 1. Load Documents
    print(f"\n[1/3] Loading PDFs from {settings.data_dir}")
    try:
        loader = DirectoryLoader(
            str(settings.data_dir), 
            glob="*.pdf", 
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        documents = loader.load()
        
        if not documents:
            print("❌ No PDFs found! Add some files to the /data folder.")
            return
        
        print(f"✅ Loaded {len(documents)} documents")
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        return

    # 2. Split Text (Chunking)
    print(f"\n[2/3] Splitting documents into chunks")
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,  # Increased overlap for better context
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks from {len(documents)} documents")
    except Exception as e:
        print(f"❌ Error splitting documents: {e}")
        return

    # 3. Create Vector Store (ChromaDB)
    print(f"\n[3/3] Creating vector database at {settings.db_dir}")
    try:
        # Note: Using FakeEmbeddings for demo. Replace with real embeddings for production.
        # Example: OpenAIEmbeddings(model="text-embedding-3-small")
        embeddings = FakeEmbeddings(size=1536)
        
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(settings.db_dir),
            collection_name="enterprise_documents"
        )
        
        # Test the database
        test_results = vector_db.similarity_search("test", k=1)
        print(f"✅ Vector database created successfully")
        print(f"   - Total chunks: {len(chunks)}")
        print(f"   - Database location: {settings.db_dir}")
        print(f"   - Test query returned: {len(test_results)} result(s)")
        
    except Exception as e:
        print(f"❌ Error creating vector database: {e}")
        return
    
    print("\n" + "=" * 60)
    print("✅ Ingestion Complete!")
    print("=" * 60)

if __name__ == "__main__":
    run_ingestion()