# 🚀 MCP AI Assistant

### Multi-Server Tool-Enabled AI System using MCP, FastAPI & Streamlit

An enterprise-style AI assistant built using the **Model Context Protocol (MCP)** architecture.

This system connects:

* 🎨 **Streamlit Frontend** (User Interface)
* ⚡ **FastAPI Backend API Layer**
* 🧠 **Async MCP Client (LLM + Tool Orchestration)**
* 🛠️ **Multiple MCP Servers (Desktop + Expense Database)**

Designed with production-level architecture principles and modular scalability.

---

# 🏗️ System Architecture

## 🔷 High-Level Architecture

```
                ┌────────────────────────────┐
                │        Streamlit UI        │
                │   (Human-like Chat UI)     │
                └───────────────┬────────────┘
                                │ HTTP Request
                                ▼
                ┌────────────────────────────┐
                │          FastAPI           │
                │     Backend API Gateway    │
                └───────────────┬────────────┘
                                │ Async Call
                                ▼
                ┌────────────────────────────┐
                │         MCP Client         │
                │  LLM + Tool Decision Logic │
                └───────────────┬────────────┘
                                │ MCP Protocol
                                ▼
        ┌──────────────────────────────────────────┐
        │              MCP Servers                 │
        │  • Desktop File Operations Server        │
        │  • Expense Database Management Server    │
        └──────────────────────────────────────────┘
```

---

# 🔄 System Flow

### 1️⃣ User Interaction

User sends message via Streamlit UI.

### 2️⃣ API Layer

FastAPI receives full session conversation.

### 3️⃣ MCP Client Processing

The async MCP client:

* Binds tools to LLM
* Detects tool calls
* Executes tools dynamically
* Feeds tool results back to model
* Generates final structured response

### 4️⃣ Tool Execution

Connected MCP servers execute:

* File operations on Desktop
* Expense management in database

### 5️⃣ Response Delivery

Final AI response is returned to Streamlit and displayed in human-style chat format.

---

# 🧠 MCP Client (Core Intelligence Layer)

The MCP Client is responsible for:

* Async execution
* Tool binding with LLM
* Tool call detection
* Secure tool invocation
* Multi-server orchestration
* Context-aware conversation handling

### Key Characteristics

* Uses `async/await`
* Supports multi-server MCP configuration
* Binds tools dynamically
* Sends full session history for context
* Returns structured AI responses

---

# 🛠️ Connected MCP Servers

## 1️⃣ Desktop MCP Server

Handles secure file operations:

* `read_file`
* `write_file`
* `delete_file` (strict confirmation)
* Path validation
* Safe directory resolution

## 2️⃣ Expense Database MCP Server

Handles financial records:

* Add expenses
* View expenses
* Delete expenses
* Manage expense database
---

# 💬 Frontend (Streamlit)

The frontend provides:

* Human-like chat interface
* Persistent session memory
* Full conversation context sending
* Real-time interaction
* Clean and minimal UI

---

# ⚡ Backend (FastAPI)

FastAPI acts as:

* API gateway
* Async bridge between UI and MCP client
* Stateless request handler
* Context forwarder

---

# 📂 Project Structure

```
MCP_CLIENT_-_FRONTEND/
│
├── fastapi_backend.py                # FastAPI backend API layer
├── fastapi_frontend.py           # Streamlit chat UI
├── client/mcp_client.py         # Async MCP client logic
├── .env                  # Environment variables
├── .gitignore
└── README.md
```

---

# 🔐 Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/umerrafiq04/MCP_CLIENT_-_FRONTEND.git
cd MCP_CLIENT_-_FRONTEND
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Start FastAPI Backend

```bash
uvicorn api:app --reload
```

Runs on:

```
http://127.0.0.1:8000
```

---

## 5️⃣ Start Streamlit Frontend

```bash
streamlit run frontend.py
```

---

# 🔒 Security Measures

* Desktop path resolution protection
* Prevents path traversal attacks
* Strict delete confirmation
* Controlled file extension handling
* Environment variable isolation
* Tool-level validation

---

# 🏢 Engineering Principles Used

* Separation of concerns
* Async architecture
* Tool-based AI orchestration
* Modular MCP server design
* Stateless API gateway
* Context-aware LLM usage
* Production-ready layering

---

# 📈 Scalability Design

The architecture supports:

* Adding new MCP servers
* Adding new tools without frontend modification
* Replacing LLM model easily
* Deploying API and UI separately
* Multi-user session expansion
* Database-backed memory integration

---

# 🚀 Future Improvements

* Streaming token responses
* Redis-backed memory
* Multi-user session isolation
* Authentication layer
* Docker containerization
* Cloud deployment (AWS / GCP)
* CI/CD integration

---

# 🧪 Example Use Cases

* Desktop file automation
* Personal AI assistant
* Financial tracking system
* Tool-based LLM experimentation
* MCP protocol experimentation platform

---

# 👨‍💻 Author

**Umer Rafiq**
BTech CSE 

---


# 🌟 Summary

This project demonstrates a fully functional, multi-server MCP-based AI system with:

✔ Clean architecture
✔ Async tool execution
✔ Real-world file & database operations
✔ Professional engineering practices
✔ Production-ready structure

---

# 🔗 Related Repositories

This repository is part of a larger MCP architecture:

- 🧠 **MCP Client (Async Tool Orchestration)**  
  https://github.com/umerrafiq04/MCP_CLIENT

- 🛠️ **MCP Server (Tool Execution Layer)**  
  https://github.com/umerrafiq04/MCP_SERVER

---


