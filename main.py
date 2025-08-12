# main.py

import os
import json
import sqlite3
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool

# --- 1. Database Setup Function ---
def setup_database():
    """Creates the SQLite database and backlog table if they don't exist."""
    conn = sqlite3.connect('backlog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS backlog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            reach INTEGER NOT NULL,
            impact REAL NOT NULL,
            confidence REAL NOT NULL,
            effort REAL NOT NULL,
            rice_score REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


# --- 2. Tool Definitions ---
@tool
def score_rice_tool(name: str, reach: int, impact: float, confidence: float, effort: float) -> str:
    """Calculates the RICE score for a given backlog item."""
    if effort == 0:
        return "Error: Effort cannot be zero."
    rice_score = (reach * impact * confidence) / effort
    return (
        f"The RICE score for '{name}' is {rice_score:.2f}. "
        f"Breakdown: [Reach: {reach}, Impact: {impact}, "
        f"Confidence: {confidence}, Effort: {effort}]"
    )

@tool
def add_item_to_backlog_tool(name: str, reach: int, impact: float, confidence: float, effort: float, rice_score: float) -> str:
    """Saves a scored feature and its RICE score to the persistent backlog database."""
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO backlog (name, reach, impact, confidence, effort, rice_score) VALUES (?, ?, ?, ?, ?, ?)",
            (name, reach, impact, confidence, effort, rice_score)
        )
        conn.commit()
        conn.close()
        return f"Successfully added '{name}' to the backlog with RICE score {rice_score:.2f}."
    except Exception as e:
        return f"Error adding item to backlog: {e}"

@tool
def view_backlog_tool() -> str:
    """Retrieves and displays all items from the backlog, sorted by the highest RICE score."""
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, rice_score FROM backlog ORDER BY rice_score DESC")
        items = cursor.fetchall()
        conn.close()
        if not items:
            return "The backlog is currently empty."
        formatted_items = "\n".join([f"- {name} (RICE Score: {score:.2f})" for name, score in items])
        return f"Current Backlog (Prioritized by RICE):\n{formatted_items}"
    except Exception as e:
        return f"Error viewing backlog: {e}"

# --- 3. Agent Setup ---
def main():
    # Run the database setup function at the start
    setup_database()

    load_dotenv()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # Add the new tools to the agent's toolbox
    tools = [score_rice_tool, add_item_to_backlog_tool, view_backlog_tool]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful product manager assistant. After scoring a feature, ask the user if they want to add it to the backlog."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # --- Use the agent interactively ---
    print("Mini-Me PM Agent is ready. Type 'exit' to end.")
    while True:
        user_request = input("You: ")
        if user_request.lower() == 'exit':
            break
        
        result = agent_executor.invoke({"input": user_request})
        print(f"Mini-Me: {result['output']}")

if __name__ == "__main__":
    main()