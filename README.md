# enterprise-research-agent


# 📂 Enterprise Research Agent

An intelligent, agentic RAG (Retrieval-Augmented Generation) system designed to conduct autonomous research across unstructured enterprise documents. This project leverages **AutoGen** for multi-agent orchestration and **LangChain** for robust document retrieval.

## 🚀 Overview

Traditional RAG systems are often linear. The **Enterprise Research Agent** introduces an "Agentic" layer where a specialized **Researcher Agent** autonomously decides when to query the knowledge base, how to refine search terms, and how to synthesize complex findings into a final report.

### Key Features

* **Autonomous Research:** Uses AutoGen agents to coordinate multi-step reasoning.
* **Semantic Retrieval:** Powered by LangChain and ChromaDB for high-accuracy document search.
* **Production-Ready API:** Served via FastAPI for seamless integration with external applications.
* **Interactive UI:** Built with Streamlit for a user-friendly research experience.

---

## 🛠️ Tech Stack

* **Language:** Python
* 
**Orchestration:** AutoGen 


* 
**RAG Framework:** LangChain 


* 
**Vector Database:** ChromaDB 


* 
**LLM API:** OpenAI (GPT-4o via Azure/GitHub Models) 


* 
**Backend:** FastAPI 


* 
**Frontend:** Streamlit 



---

## 📂 Project Structure

```text
enterprise-research-agent/
├── src/
│   ├── api.py          # FastAPI application entry point
│   ├── main.py         # Agent orchestration and logic
│   ├── agents.py       # AutoGen agent and tool definitions
│   ├── ingest.py       # Document processing and vectorization
│   └── config.py       # Pydantic settings and environment management
├── data/               # Source PDFs for ingestion
├── chroma_db/          # Local vector database storage
├── .env                # API keys and environment variables
└── requirements.txt    # Project dependencies

```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Mubrix2/enterprise-research-agent.git
cd enterprise-research-agent

```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```text
GITHUB_TOKEN=your_github_token_here
DB_DIR=./chroma_db
DATA_DIR=./data

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## 🧪 Usage

### Phase 1: Ingest Documents

Place your enterprise PDFs in the `/data` folder and run the ingestion script:

```bash
python -m src.ingest

```

### Phase 2: Start the API (Backend)

```bash
python -m src.api

```

### Phase 3: Launch the UI (Frontend)

```bash
streamlit run src/app.py

```

---

## 🤖 Agentic Workflow

1. **User Input:** The user asks a complex question via the Streamlit UI.
2. **Orchestration:** The `UserProxyAgent` initiates a chat with the `ResearcherAgent`.
3. **Tool-Calling:** The `ResearcherAgent` determines if it needs more information and calls the `query_pdfs` tool.
4. 
**Retrieval:** LangChain searches the ChromaDB for relevant document chunks. 


5. 
**Synthesis:** The agent synthesizes the retrieved context into a comprehensive answer. 



---

## 👨‍💻 Author

**Mubarak Olalekan Oladipo** 

* 
**LinkedIn:** [mubarak-oladipo](https://www.linkedin.com/in/mubarak-oladipo) 


* 
**GitHub:** [Mubrix2](https://www.google.com/search?q=https://github.com/Mubrix2) 

