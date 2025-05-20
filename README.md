# 🧠 Mach-AI Project Planner API

A FastAPI backend that uses OpenAI Function Calling to extract structured project plans from natural language. Ideal for Gantt chart generation, Bubble.io integrations, and structured project automation.

## 🚀 Features

- ✅ Natural language → structured project plans
- 🧠 GPT-4 Function Calling support
- 📅 Gantt-friendly output: phases, tasks, dates
- ⚙️ FastAPI backend with Swagger UI
- 🐳 Docker-compatible deployment


## 🔧 Setup Instructions

### 🔹 Option 1: Local Development (venv + Uvicorn)

1. Clone Repo & Create Environment

```bash
git clone https://github.com/Yixuehahaha/Mach-AI_Gen_AI.git
cd Mach-AI_Gen_AI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Add `.env` File

```bash
cp .env.example .env
```

Edit `.env` to include your OpenAI key:

```
OPENAI_API_KEY=sk-...
```

3. Run Server

```bash
uvicorn app.main:app --reload
```

Then visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🐳 Option 2: Docker Deployment

1. Build Docker Image

```bash
docker build -t mach-ai-planner .
```

2. Run the Container

```bash
docker run --env-file .env -p 8000:8000 mach-ai-planner
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ▶️ Example Flow

1. `POST /recommend` → Input your prompt (e.g., "How to build a house in California") → Returns a natural language project plan

2. `POST /dataframe/generation?user_id=...` → Converts latest recommendation to structured JSON (phases, tasks, dates)



---

## 📄 License

⚠️ This project is free for **personal, academic, and research use**, but **not licensed for commercial use**.

© 2025 Mach-AI. All rights reserved.
