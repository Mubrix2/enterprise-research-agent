# 🧠 Enterprise Deep-Research Agent

An automated Research-as-a-Service (RaaS) platform that leverages **Microsoft AutoGen**, **FastAPI**, and **Streamlit** to perform intelligent document analysis. This system uses a multi-agent orchestration pattern to ingest PDF documents, index them into a vector database, and perform context-aware research.

---

# 🤖 Project Demo
Here is the autonomous agent in action:

![Watch the demo](./assets/demo.mp4)

## 🚀 Key Features

* **Multi-Agent Orchestration**: Utilizes Microsoft AutoGen to manage a "Researcher" assistant and a "UserProxy" for tool execution.
* **Production-Ready RAG**: Full Retrieval-Augmented Generation pipeline using LangChain and ChromaDB.
* **Decoupled Architecture**: Clean separation between the AI logic (Backend API) and the User Experience (Streamlit).
* **Fully Dockerized**: Seamless deployment using Docker Compose for both backend and frontend services.
* **Document Lifecycle Management**: Upload, process, and index PDFs directly through the UI.

---

## 🛠️ Technical Stack

| Component | Technology |
| --- | --- |
| **Agent Framework** | Microsoft AutoGen |
| **Backend API** | FastAPI, Uvicorn |
| **Frontend UI** | Streamlit |
| **Vector Database** | ChromaDB |
| **Orchestration** | LangChain |
| **Deployment** | Docker, Docker Compose |
| **Language** | Python 3.12 |

---

## 📁 Project Structure

```text
├── src/
│   ├── api.py          # FastAPI application & REST endpoints
│   ├── main.py         # Agent orchestration logic
│   ├── agents.py       # AutoGen agent & tool definitions
│   ├── ingest.py       # Document processing pipeline
│   ├── config.py       # Pydantic settings management
│   └── app.py          # Streamlit dashboard
├── data/               # Source PDFs for ingestion
├── chroma_db/          # Persistent vector storage
├── docker-compose.yml  # Multi-container configuration
└── Dockerfile          # Shared environment for API & UI

```

---

## ⚙️ Setup & Installation

### 1. Prerequisites

* Docker and Docker Compose installed.
* A GitHub Personal Access Token (for the Azure/GitHub Models inference).

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
GITHUB_TOKEN=your_token_here
API_URL=http://api:8000

```

### 3. Deployment

Spin up the entire stack with a single command:

```bash
docker-compose up --build

```

* **Streamlit UI**: `http://localhost:8501`
* **FastAPI Docs**: `http://localhost:8000/docs`

---

## 🤖 How It Works

1. **Ingestion**: Documents are placed in the `/data` folder. The `ingest.py` script splits the text into chunks and generates vector embeddings.
2. **Research Query**: When a user submits a question, the **UserProxy** agent triggers the `query_knowledge_base` tool.
3. **Synthesis**: The **Researcher** agent receives the retrieved document chunks, analyzes the content, and synthesizes a comprehensive answer.
4. **Termination**: The agents continue the dialogue until a final answer is reached, marked by the `TERMINATE` signal.

---

## 📈 Future Roadmap

* [ ] Implement **HuggingFace** local embeddings to replace FakeEmbeddings.
* [ ] Add **asynchronous support** for long-running research tasks.
* [ ] Integrate **web search** tools to supplement internal document knowledge.
* [ ] Support for **Excel and Markdown** file ingestion.


