# tools/task_manager.py

import sqlite3
from datetime import date
from typing import Optional
from langchain.tools import tool

# Note: These imports are needed for the semantic search tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import numpy as np

@tool
def add_task_tool(description: str, due_date: Optional[str] = None) -> str:
    """Adds a new task to the task list. A due_date can be optionally provided in YYYY-MM-DD format."""
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (description, due_date) VALUES (?, ?)",
            (description, due_date)
        )
        conn.commit()
        conn.close()
        return f"Successfully added task: '{description}'."
    except Exception as e:
        return f"Error adding task: {e}"

@tool
def view_tasks_tool(filter_type: str) -> str:
    """
    Views tasks. filter_type must be one of ['all', 'today', 'overdue'].
    'all' shows all active tasks.
    'today' shows tasks due today.
    'overdue' shows tasks past their due date.
    """
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        today = date.today().isoformat()
        
        if filter_type == 'today':
            query = "SELECT id, description, due_date FROM tasks WHERE status = 'active' AND due_date = ?"
            params = (today,)
        elif filter_type == 'overdue':
            query = "SELECT id, description, due_date FROM tasks WHERE status = 'active' AND due_date < ?"
            params = (today,)
        elif filter_type == 'all':
            query = "SELECT id, description, due_date FROM tasks WHERE status = 'active' ORDER BY due_date"
            params = ()
        else:
            return "Error: Invalid filter type. Use 'all', 'today', or 'overdue'."

        cursor.execute(query, params)
        tasks = cursor.fetchall()
        conn.close()

        if not tasks:
            return "No tasks found for this filter."
        
        formatted_tasks = "\n".join([f"  - ID {id}: {desc} (Due: {due or 'N/A'})" for id, desc, due in tasks])
        return f"Your tasks:\n{formatted_tasks}"
    except Exception as e:
        return f"Error viewing tasks: {e}"

@tool
def mark_task_done_tool(task_id: int) -> str:
    """Marks a task as 'done' using its unique ID, effectively removing it from the active list."""
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return f"Error: No task found with ID {task_id}."
        conn.close()
        return f"Successfully marked task {task_id} as done."
    except Exception as e:
        return f"Error updating task: {e}"

@tool
def find_task_by_description_tool(description_query: str) -> str:
    """
    Finds the most similar active task based on a description query.
    Use this to find a task's ID before deleting it.
    """
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, description FROM tasks WHERE status = 'active'")
        tasks = cursor.fetchall()
        conn.close()

        if not tasks:
            return "There are no active tasks to search."

        task_list = [{"id": task[0], "content": task[1]} for task in tasks]
        texts = [task["content"] for task in task_list]

        # Use embeddings and FAISS for semantic search
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectorstore = FAISS.from_texts(texts, embeddings)
        results = vectorstore.similarity_search(description_query, k=1)

        if not results:
            return "No similar task found."

        best_match_content = results[0].page_content
        # Find the ID corresponding to the best match
        best_match_id = next((task["id"] for task in task_list if task["content"] == best_match_content), None)

        return f"Best match found: '{best_match_content}' (ID: {best_match_id}). Please confirm this is the correct task before acting on it."
    except Exception as e:
        return f"Error finding task: {e}"