# 🚀 MCP AI Assistant
*Demo Screenshots at end
### Multi-Server Tool-Enabled AI System using MCP, LangGraph, FastAPI & Streamlit

An enterprise-style AI assistant built using the **Model Context Protocol (MCP)** architecture and enhanced with **LangGraph-based orchestration**.

This system demonstrates a production-grade AI architecture combining:

* Tool-enabled LLM reasoning
* Multi-server MCP integration
* Secure file operations
* PDF intelligence workflows
* Database-backed expense tracking
* Modular and scalable design

Designed with real-world engineering principles and layered system architecture.

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
                │         LangGraph          │
                │  LLM + Tool Orchestration  │
                └───────────────┬────────────┘
                                │ MCP Protocol
                                ▼
        ┌──────────────────────────────────────────┐
        │              MCP Servers                 │
        │  • Desktop File Operations Server        │
        │  • PDF Processing Server                 │
        │  • Expense Database Management Server    │
        └──────────────────────────────────────────┘
```

---

# 🔄 System Flow

### 1️⃣ User Interaction

User sends a message via the Streamlit UI.

### 2️⃣ API Layer

FastAPI receives the full session conversation and forwards it to the LangGraph execution layer.

### 3️⃣ LangGraph Orchestration

LangGraph is responsible for:

* Binding MCP tools dynamically to the LLM
* Detecting tool calls automatically
* Routing execution to the appropriate MCP server
* Feeding tool results back into conversation state
* Generating a structured final response

This removes manual tool-loop logic and enables scalable multi-step reasoning.

### 4️⃣ Tool Execution

Connected MCP servers execute domain-specific operations:

* Secure file operations on Desktop
* PDF reading and structured document analysis
* Expense management in database

### 5️⃣ Response Delivery

The final AI response is returned to Streamlit and displayed in a human-style chat format.

---

# 🧠 LangGraph (Core Intelligence & Orchestration Layer)

LangGraph acts as the structured reasoning engine between the LLM and external tools.

### Responsibilities:

* Tool call detection
* Conditional routing
* Async tool execution
* State management
* Multi-step reasoning
* Context-aware conversation handling

### Key Characteristics

* Uses async/await
* Dynamically binds tools
* Supports multi-server MCP configuration
* Sends full session history for contextual reasoning
* Eliminates manual while-loop tool execution

---

# 🛠️ Connected MCP Servers

## 1️⃣ Desktop MCP Server

Handles secure file operations:

* `read_file`
* `write_file`
* `delete_file` (strict confirmation)
* Path validation
* Safe directory resolution

Used for:

* Saving generated receipts
* Managing automation files
* Controlled Desktop operations

---

## 2️⃣ PDF Processing MCP Server

Dedicated to document-based workflows:

* Read and extract content from PDF files
* Analyze technical skills from documents
* Support structured data extraction
* Perform document-driven automation

Used for:

* Skill extraction
* Learning roadmap generation
* AI-driven document intelligence

---

## 3️⃣ Expense Database MCP Server

Handles financial record management:

* Add expenses
* View expenses
* Delete expenses
* Manage structured expense database

Used for:

* Logging AI-estimated costs
* Skill development tracking
* Financial automation workflows

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
* Async bridge between UI and LangGraph
* Stateless request handler
* Context forwarder

---

# 📂 Project Structure

```
MCP_CLIENT_-_FRONTEND/
│
├── fastapi_backend.py        # FastAPI backend API layer
├── fastapi_frontend.py       # Streamlit chat UI
├── logic/app.py              # LangGraph orchestration layer
├── client/mcp_client.py      # Async MCP client logic
├── .env
├── .gitignore
└── README.md
```

---

# 🖼️ Demo Screenshots

## Example Prompt

<img width="1920" height="1008" alt="MCP AI Assistant - Google Chrome 17-02-2026 00_23_52" src="https://github.com/user-attachments/assets/a9c2a7b9-699d-4aee-a171-675aa1097199" />


## AI Response
<img width="1920" height="1008" alt="MCP AI Assistant - Google Chrome 17-02-2026 00_24_03" src="https://github.com/user-attachments/assets/60f4411a-c05c-4cae-801d-bd2e37425063" />


## File Creation & Database Logging
<img width="1920" height="1008" alt="fastapi_backend py - frontend2 - Visual Studio Code 17-02-2026 00_24_36" src="https://github.com/user-attachments/assets/a99704da-3c5a-4dc0-9ef6-7e58941911f5" />
<img width="1920" height="1010" alt="skill_mastery_receipt txt - Notepad 17-02-2026 00_24_48" src="https://github.com/user-attachments/assets/2c681ce0-811d-49f4-a7a1-6669b4b85cd9" />

---

# 🔐 Security Measures

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
* Production-ready layered architecture

---

# 📈 Scalability Design

The architecture supports:

* Adding new MCP servers
* Adding new tools without frontend modification
* Replacing LLM models easily
* Deploying API and UI separately
* Multi-user session expansion
* Database-backed memory integration
---
# 🧪 Example Use Cases

* Desktop file automation
* AI-driven PDF skill extraction
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

This project demonstrates a fully functional, multi-server MCP-based AI system enhanced with LangGraph orchestration:

✔ Clean architecture
✔ Async tool execution
✔ Multi-server integration
✔ Real-world file & database operations
✔ Structured LLM reasoning
✔ Production-ready design

---

# 🔗 Related Repositories

This repository is part of a larger MCP architecture ecosystem:

🧠 **MCP Client (Async Tool Orchestration)**
[https://github.com/umerrafiq04/MCP_CLIENT](https://github.com/umerrafiq04/MCP_CLIENT)

🛠️ **MCP Server (Tool Execution Layer)**
[https://github.com/umerrafiq04/MCP_SERVER](https://github.com/umerrafiq04/MCP_SERVER)

---

