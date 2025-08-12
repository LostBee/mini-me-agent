# tools/backlog_manager.py

import sqlite3
from langchain.tools import tool

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