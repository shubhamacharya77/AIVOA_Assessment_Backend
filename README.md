# Pharmaceutical QA AI Agent - Backend

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
graph TD
    A[Client UI] -->|JWT Auth| B(Auth Router)
    A -->|Chat Message| C(Chat Router)
    A -->|Complaint JSON| D(Complaint Router)
    
    subgraph FastAPI Backend
        B -->|Hash/Verify| B1[Auth Service]
        B1 -->|Query| DB[(PostgreSQL DB)]
        
        C -->|State| C1[LangGraph Complaint Agent]
        C1 -->|LLM Call| LLM1{OpenAI GPT-4o-mini}
        LLM1 -->|Ask User| C1
        LLM1 -->|Extract JSON| C1
        
        D -->|Validate| D1[Complaint Service]
        D1 -->|Invoke| D2[Risk Agent]
        D2 -->|Structured Prompt| LLM2{OpenAI GPT-4o-mini}
        LLM2 -->|Risk Assessment| D2
        D2 -->|Merge Data| D1
        D1 -->|Save Record| DB
    end
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
