# 🤖 AI Analytics Agent System

Welcome to the **AI Analytics Agent System** – an intelligent, modular application designed to provide **natural language analytics** for tabular data, unstructured documents, and SQL databases. Built on top of **LangChain**, **OpenAI GPT-4o-mini**, and integrated with a modern **Streamlit UI**, this project allows you to interact with your data using simple, conversational prompts.

---

## 📌 Table of Contents

- [🚀 Project Overview](#-project-overview)
- [🎯 Key Features](#-key-features)
- [🧠 Agents in Detail](#-agents-in-detail)
  - [📊 Data Analytics Agent](#-data-analytics-agent)
  - [📚 Context Agent](#-context-agent)
  - [🗃️ SQL Agent](#-sql-agent)
- [🧱 System Architecture](#-system-architecture)
- [🛠️ Technologies Used](#-technologies-used)
- [🔐 Authentication System](#-authentication-system)
- [🌐 API Endpoints](#-api-endpoints)
- [🖥️ Streamlit UI](#️-streamlit-ui)
- [⚙️ Environment Configuration](#️-environment-configuration)
- [📦 Project Structure](#-project-structure)
- [📈 Future Enhancements](#-future-enhancements)
- [📥 Installation & Setup](#-installation--setup)
- [✅ Run Instructions](#-run-instructions)
- [📃 License](#-license)
- [📫 Contact](#-contact)

---

## 🚀 Project Overview

The **AI Analytics Agent System** aims to democratize data analysis by enabling users to interact with various data types using **natural language queries**. Whether it's a CSV, a long text document, or a relational database, the system intelligently interprets your question and provides meaningful insights.

The system is designed to be:

- 💡 **Modular** – Each agent operates independently.
- 🛡️ **Secure** – Token-based authentication built-in.
- 🧩 **Scalable** – Easy to extend with more agents or features.
- 🎯 **Goal-Oriented** – Designed for analysts, data scientists, and domain experts who want insights without writing code.

---

## 🎯 Key Features

✨ **Highlights of the Project:**

- ✅ Natural Language Interface for querying structured & unstructured data
- 🧠 Powered by GPT-4o-mini via LangChain for reasoning & analytics
- 🔎 RAG-based search on documents using FAISS & OpenAIEmbeddings
- 🗃️ SQL querying with schema understanding and response generation
- 📊 Pandas integration for DataFrame analysis
- 🧱 Modular backend built with FastAPI
- 🖥️ Clean Streamlit UI with chat interface
- 🔐 Auth token system for secure access
- 🧠 Embedding caching for optimized performance
- 🔧 Easy-to-use and extensible codebase

---

## 🧠 Agents in Detail

### 📊 Data Analytics Agent

- 📁 Uploads tabular files (CSV, Excel)
- 🧮 Converts questions to `pandas` queries
- 📢 Uses `ChatOpenAI` for LLM-powered analysis
- 📝 Multi-turn conversational support
- 🛠️ Code in: `llm_agent.py`
  
![Data Analytics Agent](https://github.com/sagar-maru/Data-Analytics-Agent-Systems/blob/main/Project%20Documentation%20-%20Video%20-%20Images/Images/UI_DataFrame_Agent_With_Chat_History.png)

### 📚 Context Agent

- 📜 Uploads text documents (.txt)
- 📐 Chunks and embeds text using `OpenAIEmbeddings`
- 🔍 Stores embeddings in FAISS for RAG search
- 💬 Allows natural language question-answering
- 🛠️ Code in: `rag_agent.py`

![Context Agent](https://github.com/sagar-maru/Data-Analytics-Agent-Systems/blob/main/Project%20Documentation%20-%20Video%20-%20Images/Images/UI_Context_Agent_With_Chat_Summarization%20.png)

### 🗃️ SQL Agent

- 🗄️ Accepts SQLite DB files
- 🧠 Understands schema and table relationships
- 📊 Executes intelligent SQL queries via LangChain
- 🔎 Returns insights + actual SQL code
- 🛠️ Code in: `sql_agent.py`

![SQL Agent](https://github.com/sagar-maru/Data-Analytics-Agent-Systems/blob/main/Project%20Documentation%20-%20Video%20-%20Images/Images/UI_SQL_Agent_Chat_Prompt.png)

---

## 🧱 System Architecture

```

User Interface (Streamlit)
⬇
FastAPI Backend
⬇
┌─────────────┬────────────┬─────────────┐
│ Data Agent  │ SQL Agent  │ Context Agent │
└─────────────┴────────────┴─────────────┘
⬇                ⬇               ⬇
Pandas           LangChain       FAISS + Embeddings

````

- Each component operates independently for modular scalability.
- APIs are secured with auth tokens.
- State management with `st.session_state`.

---

## 🛠️ Technologies Used

| 🔧 Component       | 🧰 Technology               |
|-------------------|----------------------------|
| 🧠 LLM             | OpenAI GPT-4o-mini         |
| 🧠 LangChain       | Chains & Memory            |
| 🔤 Embeddings      | OpenAIEmbeddings           |
| 🧮 Data Handling   | Pandas                     |
| 🔍 Vector Store    | FAISS                      |
| 🌐 Backend         | FastAPI                    |
| 🖥️ Frontend        | Streamlit                  |
| 🔐 Auth            | Bearer Token Auth          |
| 📦 Dependency Mgmt | `requirements.txt`         |

---

## 🔐 Authentication System

Every API call is protected by a **Bearer Token** system:

- 🪪 Tokens generated using `SECRET_ID` & `SECRET_KEY`
- ⏰ Default expiry: 1 hour
- 🔄 Refresh tokens automatically before expiry
- 🔐 Stored in Streamlit session state

![Authentication System](https://github.com/sagar-maru/Data-Analytics-Agent-Systems/blob/main/Project%20Documentation%20-%20Video%20-%20Images/Images/APIs_Token_Based_Authentication.png)

---

## 🌐 API Endpoints

Here are the available endpoints in the backend (FastAPI):

| 📌 Endpoint         | 📄 Description                      |
|--------------------|-------------------------------------|
| `/auth/token`      | Generate authentication token       |
| `/update-df`       | Upload DataFrame file               |
| `/update-context`  | Upload text document                |
| `/update-sql`      | Upload SQLite DB                    |
| `/chat`            | Query DataFrame                     |
| `/context`         | Query document (RAG)                |
| `/sql`             | Query SQL database                  |

![API Endpoints](https://github.com/sagar-maru/Data-Analytics-Agent-Systems/blob/main/Project%20Documentation%20-%20Video%20-%20Images/Images/APIs_Based_on_FastAPI.png)

---

## 🖥️ Streamlit UI

The UI provides a conversational interface for interaction:

- 🔼 Upload files for each agent
- 💬 Ask questions in a natural language
- 🧠 Get intelligent responses
- 📝 View conversational history
- ⏳ See loading animations while responses are processed

![Streamlit UI](https://github.com/sagar-maru/Data-Analytics-Agent-Systems/blob/main/Project%20Documentation%20-%20Video%20-%20Images/Images/User_Interface_Based_on_Streamlit.png)

---

## ⚙️ Environment Configuration

A `.env` file is required with the following keys:

```env
OPENAI_API_KEY=your_openai_key
SECRET_ID=your_secret_id
SECRET_KEY=your_secret_key
````

> 🔒 Keep this file safe and out of version control (e.g., use `.gitignore`)

---

## 📦 Project Structure

```
.
├── app
│   ├── main.py           # API logic
│   ├── llm_agent.py      # DataFrame agent
│   ├── rag_agent.py      # Context agent
│   ├── sql_agent.py      # SQL agent
├── ui
│   ├── streamlit_app.py  # Streamlit UI
├── data
│   ├── *.csv / *.txt / *.db
├── .env                  # Environment variables
├── requirements.txt      # Dependency list
```

---

## 📈 Future Enhancements

🛠️ Planned features include:

* 👥 Role-based access control (Admin/User)
* 📊 BI tool integration (Power BI, Tableau)
* 🔐 Local/private LLM model support
* 🌍 Pinecone/Chroma vectorstore integration
* 📄 PDF support for context agent
* 🎨 Custom themes & dark mode in UI
* 🧩 Plug-and-play for additional agents
* 💬 Summarization before vector embedding
* 🧠 Long-term memory with vector chaining

---

## 📥 Installation & Setup

1. 📦 Clone the repository

```bash
git clone https://github.com/your-username/ai-analytics-agent.git
cd ai-analytics-agent
```

2. 🧪 Create virtual environment and activate

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. 📥 Install dependencies

```bash
pip install -r requirements.txt
```

4. 🔑 Set environment variables

Create a `.env` file in the root folder with your OpenAI and token credentials.

---

## ✅ Run Instructions

**🧠 Start the API Server:**

```bash
uvicorn app.main:app --reload
```

**🖥️ Launch the Streamlit UI:**

```bash
streamlit run ui/streamlit_app.py
```

> 📝 Make sure ports are free (e.g., 8501 for Streamlit, 8000 for FastAPI)

---

## 📃 License

This project is open-source under the [MIT License](LICENSE). You're welcome to use, modify, and distribute it as needed.

---

## 📫 Contact

👨‍💻 Created by **Sagar Maru**

🌐 [LinkedIn Profile](https://www.linkedin.com/in/sagarmaru)  
📊 [Kaggle Notebooks](https://www.kaggle.com/marusagar)  
🐙 [GitHub Projects](https://github.com/sagar-maru)  

Feel free to reach out for collaboration, issues, or ideas!

---

> 💡 *AI Analytics Agent System brings the power of large language models to your data — whether it's a spreadsheet, a long report, or an entire database. Talk to your data today!*

---
