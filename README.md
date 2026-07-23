# Pharmaceutical QA AI Agent - Backend

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" />
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens" alt="JWT" />
</div>

<br>

This is the backend service for the Pharmaceutical Quality Assurance (QA) AI platform. It is built with **FastAPI**, **SQLModel**, and **LangGraph** to power dynamic AI workflows for capturing, processing, and analyzing pharmaceutical complaints.

## 🚀 Key Capabilities
- **AI Conversational Agent**: Powered by LangGraph, it conducts dynamic, organic conversations to extract critical structured QA data from user chat.
- **AI Risk Assessment**: Automated risk prediction engine utilizing structured LLM outputs to suggest severity, root cause hypotheses, and actionable next steps.
- **Robust API Engine**: Built with FastAPI for high concurrency, automatic OpenAPI documentation, and strict Pydantic validation.
- **Database Architecture**: PostgreSQL integrated via SQLModel for robust ORM mapping.
- **Secure Authentication**: JWT-based authentication system with robust password hashing.

---

## 🌊 User Flow
1. **Authentication**: The user (QA Agent or Customer) registers and logs in via JWT.
2. **Organic Conversation**: The user initiates a conversation via the `/api/v1/chat` endpoint, describing a pharmaceutical issue (e.g., "The blister pack was unsealed").
3. **Dynamic Extraction**: The AI asks follow-up questions organically until all 13 required standard QA fields (e.g., Batch Number, Product Name, Expiry) are successfully identified.
4. **Data Submission**: The frontend submits the fully structured complaint payload to `/api/v1/complaints`.
5. **AI Risk Assessment**: Before saving to the database, a secondary LLM Agent triggers in the background to analyze the JSON payload and generate a comprehensive Risk Assessment.
6. **Persistence**: The full record (extracted data + risk assessment) is committed to the PostgreSQL database.

---

## 🔄 Data Flow Architecture

```mermaid
sequenceDiagram
    actor User as Client UI
    participant Auth as Auth API
    participant Chat as Chat API (LangGraph)
    participant Comp as Complaint API
    participant LLM as OpenAI (GPT-4o)
    participant DB as PostgreSQL

    %% 1. Authentication Flow
    User->>Auth: POST /login (Credentials)
    Auth->>DB: Verify User
    Auth-->>User: Return JWT Token

    %% 2. Conversational Extraction Flow
    User->>Chat: POST /chat (Message + JWT)
    Chat->>LLM: Analyze Chat History & Extract
    LLM-->>Chat: Extracted JSON or Follow-up Qs
    Chat-->>User: AI Response + Live Draft Data

    %% 3. Risk Assessment & Submission Flow
    User->>Comp: POST /complaints (Final JSON)
    Comp->>LLM: Trigger Risk Agent (Analyze JSON)
    LLM-->>Comp: Structured Risk Assessment
    Comp->>DB: Save Complaint + Risk Data
    Comp-->>User: 201 Created (With AI Summary)
```

### LangGraph Agent States (`Complaint Agent`)
- **Extract Node**: Scans chat history to extract QA fields.
- **Validate Node**: Checks for missing required schema fields.
- **Ask User Node**: Prompts user organically if fields are missing.
- **Finalize Node**: Returns a completion confirmation once the schema is fully satisfied.

---

## 🛠 Tech Stack
- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL & SQLModel (SQLAlchemy)
- **AI / LLM**: LangChain, LangGraph, OpenAI (gpt-4o-mini)
- **Authentication**: JWT, pwdlib

## ⚙️ Setup & Installation

1. **Create Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/pharma_qa
   OPENAI_API_KEY=sk-your-openai-api-key
   SECRET_KEY=your_super_secret_jwt_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Run the Server**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`. 
   View the interactive Swagger UI at `http://localhost:8000/docs`.
