
## Updated README.md File 📜

# Mini-Me PM Agent 🤖

An AI-powered assistant designed to help Product Managers with their daily tasks, including feature prioritization, backlog management, meeting prep, and task tracking. This project provides both a local command-line interface (CLI) and a cloud-hosted web application for easy access.

---
## ✨ Features

* **Conversational AI:** Engage in natural, multi-turn conversations to perform tasks, with memory of the current conversation.
* **Prioritization & Backlog:**
    * Calculates a RICE score for new feature ideas.
    * Saves scored features to a persistent SQLite database.
    * Views the prioritized backlog at any time.
* **Meeting Notes Management:**
    * Add notes to specific, named meetings (e.g., "1:1 with Boss").
    * View all notes for a meeting.
    * List all meetings that have notes.
    * Delete specific notes or entire meetings.
* **Task List Management:**
    * Add new tasks with optional due dates.
    * View tasks filtered by 'all', 'today', or 'overdue'.
    * Mark tasks as 'done'.
    * **Semantic Task Search:** Find a task to act on using natural language (e.g., "the Google Analytics task") instead of just by ID.
* **Dual Interface:**
    * A local terminal version (`main.py`).
    * A web-based UI (`app.py`) built with Streamlit.
* **Automated Dependency Management:** Uses `pip-tools` for clean and reproducible builds.

---
## 🛠️ Tech Stack

* **Language:** Python
* **AI Framework:** LangChain
* **LLM:** Google Gemini (`gemini-2.5-flash`)
* **Web Framework:** Streamlit
* **Database:** SQLite
* **Vector Search:** FAISS
* **Dependency Management:** pip-tools

---
## 📂 Project Structure

.
├── tools/
│   ├── **init**.py
│   ├── backlog\_manager.py
│   ├── meeting\_manager.py
│   ├── rice\_scorer.py
│   ├── task\_manager.py
│   └── utils.py
├── .gitignore
├── app.py              \# The Streamlit web application
├── backlog.db          \# The SQLite database file
├── main.py             \# The local command-line agent
├── README.md           \# This file
├── requirements.in     \# List of top-level dependencies
├── requirements.txt    \# Auto-generated locked dependencies
└── .env                \# API keys and environment variables


---
## 🚀 Setup and Installation

Follow these steps to get the agent running on your local machine.

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd mini-me-agent
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate it (macOS/Linux)
    source venv/bin/activate

    # Activate it (Windows)
    .\venv\Scripts\activate
    ```

3.  **Set Up Your API Key**
    Create a file named `.env` in the root of the project and add your API keys. You will need keys for both Google AI and LangSmith.
    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_AI_KEY"
    LANGCHAIN_TRACING_V2="true"
    LANGCHAIN_API_KEY="YOUR_LANGSMITH_KEY"
    LANGCHAIN_PROJECT="Mini-Me PM Agent"
    ```

4.  **Install Dependencies**
    This project uses `pip-tools` for clean dependency management.
    ```bash
    # Install pip-tools itself
    pip install pip-tools

    # Compile the full requirements.txt from the .in file
    pip-compile requirements.in

    # Install all the required libraries
    pip install -r requirements.txt
    ```

---
## Usage

You can run the agent in two different ways.

### Local Command-Line Interface (CLI)
For direct interaction in your terminal. This is great for development and testing.

```bash
python main.py
````

The agent will start, and you can begin chatting with it directly in the console. Type `exit` to end the session.

### Web Application (Streamlit)

To launch the user-friendly web interface on your local machine.

```bash
streamlit run app.py
```

This command will start a local web server and open the application in your browser. This is the same code that is deployed to Streamlit Community Cloud for online access.



