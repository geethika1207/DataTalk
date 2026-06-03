# DataTalk – AI-Powered Conversational Data Analysis

DataTalk is a full-stack AI application that allows users to upload CSV datasets, ask questions in natural language, and receive data-driven insights along with automatically generated visualizations.

The goal is to make data analysis accessible to everyone—from students and non-technical users to data analysts and machine learning engineers—without requiring Python, SQL, or spreadsheet expertise.

--- 

## LIVE DEMO 
https://data-talk-1qmc.vercel.app/

**Backend**
https://datatalk-xq73.onrender.com/docs

--- 

## Problem Statement

Data analysis is often difficult for:

- Non-technical users who cannot write Python or SQL.
- Students trying to understand unfamiliar datasets.
- Data analysts who spend time on repetitive exploratory analysis.
- Machine learning practitioners who need quick dataset insights before modeling.

Most existing tools require coding knowledge or manual exploration before useful insights can be generated.

## Solution

DataTalk solves this by allowing users to upload a CSV file and ask questions in natural language.

The platform automatically analyzes the dataset, generates insights, and creates visualizations without requiring users to write code.

---

##  Key Features

###  Upload and Analyze CSV Files
Users can upload datasets directly through the web application.

###  Natural Language Data Queries
Ask questions about the data in plain English.

**Examples:**
- "Which category has the highest sales?"
- "Show revenue trends over time."
- "What patterns exist in this dataset?"

###  AI-Generated Insights
Large Language Models analyze dataset summaries and generate contextual responses.

###  Automatic Chart Generation
DataTalk generates structured chart data that is rendered dynamically on the frontend.

###  Persistent Data Storage
Uploaded datasets, chat history, and analysis results are stored in PostgreSQL.

###  Secure Authentication
JWT-based authentication system with password hashing.

--- 

##  System Architecture

```text
User Browser (Anywhere in the World)
        ↓
React Frontend (Vercel — https://data-talk-1qmc.vercel.app/)
        ↓
FastAPI Backend (Render — https://datatalk-xq73.onrender.com)
        ↓
PostgreSQL Database (Render — Managed DB)
        ↓
Groq API (Groq Cloud) / Gemini API (Google Cloud)
```
---

## Request Flow

```text
User asks a question
        ↓
Frontend sends request to FastAPI
        ↓
FastAPI retrieves dataset information
        ↓
Pandas loads and analyzes CSV data
        ↓
Dataset summary is generated
        ↓
Prompt is constructed
        ↓
Groq / Gemini processes the request
        ↓
Structured JSON response is returned
        ↓
Result is stored in PostgreSQL
        ↓
Frontend renders insights and charts
```
---

## Tech Stack

### Backend

* **FastAPI** — API framework
* **PostgreSQL** — Database
* **SQLAlchemy 1.x** — ORM
* **Pydantic** — Data validation
* **JWT (python-jose)** — Authentication
* **bcrypt (passlib)** — Password hashing
* **pandas** — CSV processing and dataset analysis
* **Groq API (LLaMA 3.3 70B)** — AI-powered insight generation

### Frontend

* **React 18** — User interface
* **Recharts** — Dynamic bar, line, and pie charts
* **DM Sans** — Typography
* **Tabler Icons** — Icon library
* **Fetch API** — Client-server communication

### AI Layer

* **Groq API**
* **Gemini API**
* **LLaMA 3.3 70B**
* **Prompt Engineering**

### Deployment

* **Frontend:** Vercel
* **Backend:** Render Web Service
* **Database:** Render PostgreSQL

---

## Challenges Faced

### 1. Production Deployment Issues

The application worked correctly in local development but encountered deployment issues on Render due to Python version compatibility. Render defaulted to Python 3.14, which caused dependency conflicts with pandas and NumPy. This was resolved by explicitly configuring the Python runtime and stabilizing package versions.

### 2. Render Ephemeral File System

Initially, uploaded CSV files were stored and processed later when users asked questions. This worked locally but failed in production because uploaded files are not permanently stored on Render's filesystem. The solution was to generate dataset summaries immediately after upload and use those summaries for future AI interactions.

### 3. Free-Tier Cold Starts

Render's free tier introduces startup delays after periods of inactivity, affecting user experience. To reduce response delays during demonstrations and testing, an uptime monitoring service was configured to keep the backend active.

### 4. AI Integration Debugging

Several deployment-specific issues emerged while connecting the AI layer, including API key configuration and environment variable management. These were resolved through production debugging and environment setup validation.  

---

## Key Learning Outcomes

* Designing scalable backend APIs with FastAPI.
* Building AI-powered data analysis workflows.
* Prompt engineering for structured AI responses.
* PostgreSQL database design using SQLAlchemy.
* JWT authentication and secure user management.
* Production deployment using Render and Vercel.
* Debugging cloud-specific issues that do not appear in local development.
* Managing AI integrations with Groq API.
* Handling real-world deployment challenges involving file storage, environment variables, and       dependency compatibility.

---

## Future Improvements

- Multi-file dataset analysis
- Automated dashboard generation
- Exportable reports (PDF and Excel)
- Advanced visualization recommendations
- Dataset comparison and benchmarking workflows
- AI-powered anomaly detection
- Team collaboration and shared workspaces 

---

## Author

**Geethika Tammineni**

Aspiring Software Engineer | Backend Development | AI-Powered Applications

Passionate about building scalable software products that leverage data, automation, and artificial intelligence to solve real-world problems.
