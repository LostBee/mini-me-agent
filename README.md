# Mini-Me PM Agent 🤖

An AI-powered assistant designed to help Product Managers with their daily tasks, including feature prioritization and backlog management. This project provides both a local command-line interface (CLI) and a cloud-hosted web application for easy access.

-----

## ✨ Features

  * **Conversational AI:** Engage in natural, multi-turn conversations to perform tasks.
  * **RICE Scoring Tool:** Automatically calculates a RICE (Reach, Impact, Confidence, Effort) score for new feature ideas to aid in prioritization.
  * **Persistent Backlog:** Stores scored features in a local SQLite database, so the agent's memory persists between sessions.
  * **Backlog Management:** View the prioritized backlog at any time, sorted by the highest RICE score.
  * **Dual Interface:**
      * A **local terminal version** (`main.py`) for development and direct interaction.
      * A **web-based UI** (`app.py`) built with Streamlit, deployed for online access.
  * **Modular Tool Architecture:** Tools are organized in separate files for clean code and easy expansion.

-----

## 🛠️ Tech Stack

  * **Language:** Python
  * **AI Framework:** LangChain
  * **LLM:** Google Gemini (`gemini-2.5-flash`)
  * **Web Framework:** Streamlit
  * **Database:** SQLite

-----

## 📂 Project Structure

```
.
├── tools/
│   ├── __init__.py
│   ├── rice_scorer.py
│   └── backlog_manager.py
├── .gitignore
├── app.py              # The Streamlit web application
├── backlog.db          # The SQLite database file
├── main.py             # The local command-line agent
├── README.md           # This file
├── requirements.txt    # Python dependencies
└── .env                # API keys and environment variables
```

-----

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

3.  **Install Dependencies**
    All required libraries are listed in `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Your API Key**
    The agent needs your Google AI API key to function.

      * Create a file named `.env` in the root of the project.
      * Add your API key to the file like this:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

-----

## Usage

You can run the agent in two different ways.

### Local Command-Line Interface (CLI)

For direct interaction in your terminal. This is great for development and testing.

```bash
python main.py
```

The agent will start, and you can begin chatting with it directly in the console. Type `exit` to end the session.

### Web Application (Streamlit)

To launch the user-friendly web interface on your local machine.

```bash
streamlit run app.py
```

This command will start a local web server and open the application in your browser. This is the same code that is deployed to Streamlit Community Cloud for online access.
