# 🚀 MCP AI Assistant

*Demo screenshots at the end*

**Multi-Server Tool-Enabled AI System using MCP,Langchain,LangGraph, FastAPI & Streamlit**

An enterprise-style AI assistant built using the **Model Context Protocol (MCP)** architecture and enhanced with **LangGraph-based orchestration**.

This system demonstrates a **production-grade AI architecture** combining:

* Tool-enabled LLM reasoning
* Multi-server MCP integration
* Local tool execution layer
* Secure file operations
* PDF intelligence workflows
* Database-backed expense tracking
* Real-time streaming responses (ChatGPT-style)
* Human-in-the-Loop safety confirmation
* Modular and scalable architecture

The project is designed using **real-world engineering principles and layered system architecture**.

---

# 🏗️ System Architecture

## 🔷 High-Level Architecture

```
                ┌────────────────────────────┐
                │        Streamlit UI        │
                │     (Human-like Chat UI)   │
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
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
        ┌───────────────────────┐       ┌─────────────────────────┐
        │   Local Tool Layer    │       │       MCP Servers        │
        │     (simple_tools)    │       │   External Tool Systems  │
        ├───────────────────────┤       ├─────────────────────────┤
        │ Tavily Web Search     │       │ Desktop Operations      │
        │ Utility helpers       │       │ PDF Processing          │
        │                       │       │ Expense Database        │
        └───────────────────────┘       └─────────────────────────┘
```

---

# 🔄 System Flow

### 1️⃣ User Interaction

The user sends a message through the **Streamlit chat interface**.

The interface supports **real-time streaming responses**, allowing users to observe the AI response as it is generated.

---

### 2️⃣ API Layer

**FastAPI** receives the full session conversation and forwards it to the **LangGraph execution layer**.

FastAPI acts as the **gateway between the frontend and the AI orchestration system**.

---

### 3️⃣ LangGraph Orchestration

LangGraph is responsible for:

* Dynamically binding MCP tools to the LLM
* Integrating local utility tools
* Detecting tool calls automatically
* Routing execution to the appropriate tool
* Feeding tool results back into the conversation state
* Generating a structured final response

This removes manual tool-loop logic and enables **scalable multi-step reasoning**.

---

### 4️⃣ Tool Execution

LangGraph can execute tools from **two different sources**.

---

## Local Tools (`simple_tools`)

These are lightweight tools implemented directly inside the project.

Examples include:

* Tavily web search tool for real-time information retrieval
* File discovery utilities
* Desktop file listing
* Helper utilities
* Lightweight automation functions

These tools are located in:

```
logic/simple_tools.py
```

---

## Remote MCP Servers

External tool systems connected through the **Model Context Protocol (MCP)**.

Connected MCP servers perform domain-specific operations such as:

* Secure file operations on Desktop
* PDF document analysis
* Expense database management

LangGraph dynamically determines whether to call a **local tool** or an **MCP server tool**.

---

### 5️⃣ Response Delivery

The final AI response is **streamed back to the Streamlit UI** and displayed in a human-like chat format.

---

# 🛡️ Human-in-the-Loop (HITL) Safety Layer

Certain operations are considered **sensitive or destructive** and require explicit human confirmation before execution.

Examples include:

* Deleting files
* Deleting multiple documents
* Creating or modifying sensitive data
* Large-scale file operations

When such actions are detected, the system **pauses execution and requests confirmation from the user**.

This ensures:

* Controlled execution of destructive actions
* Prevention of accidental data loss
* Human supervision over automated workflows
* Increased system reliability and safety

---

# ⚡ Real-Time Streaming Responses

The assistant streams responses **token-by-token**, similar to modern conversational AI systems.

### Benefits

* Faster perceived response time
* More natural conversational interaction
* Transparent AI reasoning
* Improved user experience

Streaming is implemented using:

* **FastAPI streaming responses**
* **LangGraph asynchronous execution**
* **Streamlit incremental rendering**

---

# 🧠 LangGraph

### Core Intelligence & Orchestration Layer

LangGraph acts as the **reasoning engine connecting the LLM with both local tools and MCP servers**.

### Responsibilities

* Tool call detection
* Conditional routing
* Asynchronous tool execution
* Conversation state management
* Multi-step reasoning
* Context-aware interaction

### Key Characteristics

* Uses **async/await architecture**
* Dynamically binds tools
* Integrates both **local and remote tools**
* Sends full session history for contextual reasoning
* Eliminates manual tool execution loops

---

# 🔧 Local Tool Layer

The system includes a **lightweight local tool layer** implemented directly inside the project.

**Location**

```
logic/simple_tools.py
```

These tools provide **fast utility operations without requiring external MCP servers**.

Examples include:

* File discovery tools
* Desktop file listing
* Helper utilities
* Lightweight automation functions

Local tools improve **system responsiveness** and reduce dependency on remote services.

---

# 🛠️ Connected MCP Servers

## 1️⃣ Desktop MCP Server

Handles **secure file operations**, including:

* `read_file`
* `write_file`
* `delete_file`
* `list_files`

Additional protections include:

* Path validation
* Safe directory resolution

Used for:

* Managing automation files
* Secure desktop operations
* Controlled file management

---

## 2️⃣ PDF Processing MCP Server

Dedicated to **document-based workflows**, including:

* Reading and extracting content from PDF files
* Analyzing document information
* Supporting structured data extraction
* Performing document-driven automation

Used for:

* Document intelligence
* Knowledge extraction
* AI-driven document analysis

---

## 3️⃣ Expense Database MCP Server

Handles **financial record management**, including:

* Adding expenses
* Viewing expenses
* Deleting expenses
* Managing structured expense databases

Used for:

* Logging AI-estimated costs
* Financial tracking automation
* Structured expense management

---

# 💬 Frontend (Streamlit)

The frontend provides:

* Human-like chat interface
* Persistent session memory
* Streaming responses
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
├── fastapi_backend.py          # FastAPI backend API layer
├── fastapi_frontend.py         # Streamlit chat UI
│
├── logic/
│   ├── app.py                  # LangGraph orchestration layer
│   └── simple_tools.py         # Local utility tools
│
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

## Human-in-the-Loop Confirmation

<img width="1920" height="1008" alt="Streamlit - Google Chrome 08-03-2026 01_11_02" src="https://github.com/user-attachments/assets/382a0dc2-dd16-4a38-a5bf-efeff8df90db" />
<img width="1920" height="1008" alt="Streamlit - Google Chrome 08-03-2026 01_11_29" src="https://github.com/user-attachments/assets/1d624bb8-7257-45ac-8db8-67fb4fa0236a" />
<img width="1920" height="1008" alt="Streamlit - Google Chrome 08-03-2026 01_11_40" src="https://github.com/user-attachments/assets/c4c220fc-9def-4ef1-a638-4e822327270e" />

---

# 🔐 Security Measures

* Desktop path resolution protection
* Prevention of path traversal attacks
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
* Integrating additional local tool modules
* Replacing LLM models easily
* Deploying API and UI separately
* Multi-user session expansion
* Database-backed memory integration

---

# 🧪 Example Use Cases

* Desktop file automation
* AI-driven PDF analysis
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

This project demonstrates a **fully functional multi-server MCP-based AI system enhanced with LangGraph orchestration**.

✔ Clean architecture
✔ Async tool execution
✔ Hybrid **Local + MCP tool system**
✔ Real-world file & database operations
✔ Structured LLM reasoning
✔ Human-in-the-loop safety control
✔ Real-time streaming responses
✔ Production-ready design

---

# 🔗 Related Repositories

### 🛠️ MCP Server(Tools)

[https://github.com/umerrafiq04/MCP_SERVER](https://github.com/umerrafiq04/MCP_SERVER)

