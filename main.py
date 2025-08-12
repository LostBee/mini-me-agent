# main.py

import os
import sqlite3
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, AIMessage

# --- Import the tools from their new files ---
from tools.rice_scorer import score_rice_tool
from tools.backlog_manager import add_item_to_backlog_tool, view_backlog_tool
from tools.meeting_manager import (
    add_meeting_note_tool,
    view_meeting_notes_tool,
    list_meetings_tool,
    delete_note_by_id_tool,
    delete_meeting_tool
)

# --- Database Setup Function ---
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
     # --- New Tables for Meetings ---
    # Stores the unique meeting names
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    # Stores the notes, linked to a meeting by meeting_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (meeting_id) REFERENCES meetings (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

# --- Agent Setup ---
def main():
    setup_database()

    load_dotenv()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # The tools list now uses the imported functions
    tools = [
    score_rice_tool,
    add_item_to_backlog_tool,
    view_backlog_tool,
    add_meeting_note_tool,
    view_meeting_notes_tool,
    list_meetings_tool,
    delete_note_by_id_tool,
    delete_meeting_tool
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful product manager assistant. After scoring a feature, ask the user if they want to add it to the backlog."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # --- Interactive Loop ---
    chat_history = []
    print("Mini-Me PM Agent is ready. Type 'exit' to end.")
    while True:
        user_request = input("You: ")
        if user_request.lower() == 'exit':
            break
        
        result = agent_executor.invoke({
            "input": user_request,
            "chat_history": chat_history
        })
        
        chat_history.append(HumanMessage(content=user_request))
        chat_history.append(AIMessage(content=result['output']))
        
        print(f"Mini-Me: {result['output']}")

if __name__ == "__main__":
    main()