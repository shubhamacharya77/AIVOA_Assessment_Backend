# Pharmaceutical QA AI Agent - Backend

This is the backend service for the Pharmaceutical QA AI platform. It is built with **FastAPI**, **SQLModel**, and **LangGraph** to power dynamic AI workflows.

## 🚀 Features
- **AI Agent Chat API**: LangGraph-powered conversational AI for extracting QA complaint data (source, product, severity, etc.) organically from user chat.
- **AI Risk Assessment**: Automated risk prediction engine utilizing structured LLM outputs to suggest severity, root cause hypotheses, and actionable next steps.
- **Robust API**: Built with FastAPI for high performance, automatic OpenAPI documentation, and strict Pydantic data validation.
- **Database**: PostgreSQL integrated via SQLModel for robust ORM mapping.
- **Secure Authentication**: JWT-based authentication system with password hashing.

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
