# DataTalk

## An AI-Powered Conversational Data Analysis Platform

> **Why I'm building this:** Data analysis is often restricted by a technical barrier—requiring Python, SQL, or complex spreadsheet formulas. I built DataTalk to make data instantly accessible to everyone. From students to machine learning engineers, users can simply upload a CSV and ask questions in natural language. Instead of spending hours on exploratory data analysis, the system instantly processes the dataset via a high-performance DuckDB backend and generates context-aware insights and smart visualizations, democratizing data analysis for non-technical and technical users alike.

**DataTalk** is a full-stack AI application engineered to bridge the gap between raw data and actionable intelligence. Instead of manually writing queries, the system leverages a decoupled architecture to ingest datasets, analyze them dynamically, and return structured insights alongside auto-generated Plotly visualizations.

To achieve this, I engineered a production-grade pipeline featuring a **FastAPI + DuckDB** backend for high-speed local analytical querying, coupled with the **Groq API (LLaMA)** for rapid natural language processing. The frontend is built on **Streamlit**, featuring persistent session state, scrollable chat history, and smart chart rendering (e.g., dynamically switching to horizontal bar charts for large categories) to deliver a seamless, professional user experience.

---

## 🌍 Live Deployments

Test the active platform live:

* **Frontend UI (Streamlit):** [https://datatalk-app.streamlit.app](https://www.google.com/search?q=https://datatalk-app.streamlit.app) *(Replace with your actual Streamlit link)*
* **Backend API (FastAPI Docs):** [https://datatalk-1-qlhh.onrender.com/docs](https://www.google.com/search?q=https://datatalk-1-qlhh.onrender.com/docs)

---

## 🛠️ Built With

---

## 🛠️ Technical Overview

| Category | Specification |
| --- | --- |
| Project Type | AI-Powered Data Analysis System |
| Primary Language | Python 3.11 |
| Backend Framework | FastAPI |
| Frontend Framework | Streamlit |
| Analytical Engine | DuckDB |
| Large Language Model | Groq API (LLaMA 3.3 70B) / Gemini API |
| Visualization Library | Plotly Express |
| Concurrency Model | REST API with asynchronous endpoints |
| Data Storage | PostgreSQL (User Auth) & In-memory (Dataset processing) |
| Authentication | JWT Authentication with bcrypt hashing |

---

## 🏗 System Architecture

DataTalk adopts a decoupled, microservice-style architecture that cleanly separates the heavy backend analytical engine from the lightweight frontend client.

```text
User Browser
    │
    ▼
Streamlit Frontend (Community Cloud)
(Handles session state, chat history, Plotly rendering)
    │
    ▼ [REST API / requests]
    │
FastAPI Backend (Render)
    │
    ├──► PostgreSQL (JWT Auth & User Verification)
    │
    ├──► DuckDB / Pandas (CSV Ingestion & SQL Query Execution)
    │
    └──► Groq API (Prompt Construction & Insight Generation)
    │
    ▼
Structured JSON Response (Answer + Chart Configuration)
    │
    ▼
Streamlit Renders Smart Visualizations & Metrics

```

---

## ⚙️ Key Design Choices

* **Decoupled Deployment Environment:** Completely isolated the Streamlit frontend and FastAPI backend into separate deployments. The frontend utilizes a dedicated `frontend/requirements.txt` to prevent heavy backend dependencies (like Matplotlib or Gunicorn) from crashing the UI server.
* **Smart Visualizations:** Engineered a dynamic rendering engine using Plotly. If a dataset category exceeds 10 items, it automatically defaults to a horizontal bar chart to prevent label crowding. Exact calculated totals are rendered directly on the bars for instant readability.
* **Persistent Chat History:** Replaced single-response UI states with a persistent `st.session_state.messages` array, allowing users to scroll, compare past charts, and maintain conversational context.
* **Automated Context Wiping:** Implemented a single-dataset lock per session. When a user uploads a new dataset, the system automatically clears the chat history to provide a fresh workspace and prevent metric confusion.
* **In-Memory Analytical Processing:** Utilized DuckDB and Pandas on the backend to execute lightning-fast analytical queries directly on the uploaded CSVs without requiring persistent file storage on Render's ephemeral filesystem.

---

## 🧩 Core Components

| Layer | Responsibility |
| --- | --- |
| 🎨 **Streamlit Client** | Decoupled UI managing JWT states, file uploads, persistent chat history, and rendering Plotly charts. |
| 🛡 **Auth Layer** | Secures API endpoints and manages user sessions via native JWT Authentication and password hashing. |
| 🗂 **Dataset Processor** | Parses uploaded CSV files and extracts metadata and schema summaries for the LLM context. |
| 🤖 **Groq API Engine** | Synthesizes user natural language into structured analytical queries and contextual insights. |
| 📊 **DuckDB Engine** | High-performance, in-memory SQL execution engine for rapid data aggregation. |
| 📈 **Visualization Configurator** | Backend constructs strict JSON chart configurations parsed by the frontend into interactive Plotly elements. |

---

## ⚙️ Engineering Challenges

Building a production-grade data analysis system required solving severe bottlenecks around dependency management, ephemeral cloud storage, and UI persistence.

| **⚙️ Challenge** | **🚀 Engineering Solution** |
| --- | --- |
| **Streamlit "Infinite Oven" Deployment Crash** <br>

<br> *Streamlit Cloud failed to deploy, attempting to build heavy backend libraries (like Matplotlib) on a free-tier server.* | **Decoupled Dependency Architecture:** Moved `streamlit_app.py` into a dedicated `frontend/` folder with its own lightweight `requirements.txt` (only Streamlit, requests, pandas, plotly), bypassing backend dependency bloat. |
| **Render Ephemeral File System** <br>

<br> *CSV files disappeared after upload because Render does not persist files across server spins.* | **Immediate Summary Processing:** Shifted the architecture to process datasets in-memory immediately upon upload, relying on DuckDB for fast aggregations without needing permanent disk storage. |
| **UI Context Loss** <br>

<br> *Asking a new question wiped the previous chart from the screen.* | **Session State Array:** Implemented a full chat history loop mapping over `st.session_state.messages` to render every historical chart and metric sequentially. |
| **Crowded Chart Labels** <br>

<br> *Categorical data with too many unique values made x-axis labels unreadable.* | **Smart Rendering Logic:** Added algorithmic checks (`len(df) > 10`) to automatically rotate charts to a horizontal orientation and format exact values directly onto the bars. |

---

## 📂 Repository Architecture

DataTalk adopts a modular architecture that cleanly separates the heavy **FastAPI** backend from the lightweight **Streamlit** client to enable seamless deployments.

```text
DataTalk/
├── app/                   # FastAPI backend application
│   ├── core/              # Security (JWT, password hashing)
│   ├── db/                # PostgreSQL & SQLAlchemy models
│   ├── routers/           # REST API endpoints (Auth, Datasets, Queries)
│   ├── schemas/           # Pydantic strict data validation
│   └── services/          # Groq integration, DuckDB logic, prompt mapping
│
├── frontend/              # Streamlit user interface
│   ├── streamlit_app.py   # Native UI, auth state, chat history, Plotly rendering
│   └── requirements.txt   # Lightweight UI dependencies (streamlit, requests, pandas, plotly)
│
├── requirements.txt       # Heavy backend dependencies (fastapi, duckdb, sqlalchemy, etc.)
├── .env                   # Environment configuration
└── README.md

```

---

## 🚀 Future Improvements

* **Multi-file Dataset Analysis:** Allow JOIN operations across multiple uploaded CSVs.
* **Automated Dashboard Generation:** Instantly compile the most important metrics upon initial file upload.
* **Exportable Reports:** One-click downloads for PDF and Excel analysis summaries.
* **AI-Powered Anomaly Detection:** Proactively highlight outliers in the dataset before the user asks.

---

## 💻 Local Setup & Execution

### Prerequisites

* Python **3.11+**
* PostgreSQL
* Groq API Key

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/<your-username>/DataTalk.git
cd DataTalk

```


2. Set up a virtual environment and install backend dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```


3. Configure your `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/datatalk
SECRET_KEY=your_jwt_secret_key

```


4. Start the FastAPI development server:
```bash
uvicorn app.main:app --reload

```


*API Docs available at: `http://localhost:8000/docs*`

### Frontend Setup

1. Open a new terminal window and navigate to the frontend folder:
```bash
cd frontend

```


2. Install the lightweight frontend dependencies (make sure your venv is active):
```bash
pip install -r requirements.txt

```


3. Run the Streamlit app:
```bash
streamlit run streamlit_app.py

```



---

## 🎯 Conclusion

**DataTalk** demonstrates how modern web frameworks and Large Language Models can be combined to entirely remove the friction from data analysis.

By unifying **FastAPI**, in-memory **DuckDB** processing, and a decoupled **Streamlit** client, this platform delivers rapid, actionable insights and professional-grade visualizations directly from natural language. From resolving complex dependency deployment clashes to engineering a smart, stateful UI, this project serves as a robust blueprint for AI-driven analytical tools.

---

**Developed by Geethika Nagasri Tammineni**

Aspiring Software Engineer | Backend Development | AI-Powered Applications

Passionate about building scalable software products that leverage data, automation, and artificial intelligence to solve real-world problems. If you found this project interesting, feel free to connect, contribute, or share feedback!
