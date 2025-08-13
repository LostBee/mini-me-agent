# app.py

import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, AIMessage

# Import your tools
from tools.rice_scorer import score_rice_tool
from tools.backlog_manager import add_item_to_backlog_tool, view_backlog_tool
from tools.meeting_manager import (
    add_meeting_note_tool,
    view_meeting_notes_tool,
    list_meetings_tool,
    delete_note_by_id_tool,
    delete_meeting_tool
    )
from tools.task_manager import (
    add_task_tool,
    view_tasks_tool,
    mark_task_done_tool,
    find_task_by_description_tool,
    )

# --- Database Setup (runs once)---
def setup_database():
    conn = sqlite3.connect('backlog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS backlog (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, reach INTEGER NOT NULL,
            impact REAL NOT NULL, confidence REAL NOT NULL, effort REAL NOT NULL,
            rice_score REAL NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# --- Agent Setup (Cached for performance) ---
# Use st.cache_resource to prevent re-creating the agent on every interaction
@st.cache_resource
def get_agent_executor():
    load_dotenv()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    tools = [
    score_rice_tool,
    add_item_to_backlog_tool,
    view_backlog_tool,
    add_meeting_note_tool,
    view_meeting_notes_tool,
    list_meetings_tool,
    delete_note_by_id_tool,
    delete_meeting_tool, 
    add_task_tool, 
    view_tasks_tool, 
    mark_task_done_tool, 
    find_task_by_description_tool
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful product manager assistant. You help with tools availble in your tools like Rice Scoring, after scoring a feature, ask the user if they want to add it to the backlog. And while working with tasks, To delete a task by description, first use the find_task_by_description_tool to get the ID, then confirm with the user before you offer to mark it as done."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Main App Logic ---
setup_database()
agent_executor = get_agent_executor()

st.title("Mini-Me PM Agent 🤖")

# Initialize chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)

# Handle new user input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to history and display it
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("human"):
        st.markdown(prompt)

    # Get agent's response
    with st.spinner("Thinking..."):
        result = agent_executor.invoke({
            "input": prompt,
            "chat_history": st.session_state.messages[:-1] # Pass history BEFORE the new user message
        })
        response = result['output']

        # Add AI response to history and display it
        st.session_state.messages.append(AIMessage(content=response))
        with st.chat_message("ai"):
            st.markdown(response)