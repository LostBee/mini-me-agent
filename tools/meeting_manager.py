# tools/meeting_manager.py

import sqlite3
from langchain.tools import tool

def _get_meeting_id(cursor, meeting_name):
    """Helper function to get or create a meeting ID."""
    cursor.execute("SELECT id FROM meetings WHERE name = ?", (meeting_name,))
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO meetings (name) VALUES (?)", (meeting_name,))
        return cursor.lastrowid
    return data[0]

@tool
def add_meeting_note_tool(meeting_name: str, content: str) -> str:
    """Adds a note to a specific meeting. Creates the meeting if it doesn't exist."""
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        meeting_id = _get_meeting_id(cursor, meeting_name)
        cursor.execute("INSERT INTO notes (meeting_id, content) VALUES (?, ?)", (meeting_id, content))
        conn.commit()
        conn.close()
        return f"Successfully added note to '{meeting_name}'."
    except Exception as e:
        return f"Error: Could not add note. {e}"

@tool
def view_meeting_notes_tool(meeting_name: str) -> str:
    """Views all notes for a specific meeting, including their IDs."""
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT n.id, n.content FROM notes n
            JOIN meetings m ON n.meeting_id = m.id
            WHERE m.name = ?
        """, (meeting_name,))
        notes = cursor.fetchall()
        conn.close()
        if not notes:
            return f"No notes found for meeting '{meeting_name}'."
        formatted_notes = "\n".join([f"  - Note ID {id}: {content}" for id, content in notes])
        return f"Notes for '{meeting_name}':\n{formatted_notes}"
    except Exception as e:
        return f"Error: Could not view notes. {e}"

@tool
def list_meetings_tool() -> str:
    """Lists all meetings that have notes."""
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM meetings ORDER BY name")
        meetings = cursor.fetchall()
        conn.close()
        if not meetings:
            return "No meetings found."
        formatted_meetings = "\n".join([f"- {name[0]}" for name in meetings])
        return f"Here are your meetings:\n{formatted_meetings}"
    except Exception as e:
        return f"Error: Could not list meetings. {e}"

@tool
def delete_note_by_id_tool(note_id: int) -> str:
    """Deletes a specific note using its unique Note ID."""
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        # Check if any row was affected
        if cursor.rowcount == 0:
            conn.close()
            return f"Error: No note found with ID {note_id}."
        conn.close()
        return f"Successfully deleted note with ID {note_id}."
    except Exception as e:
        return f"Error: Could not delete note. {e}"

@tool
def delete_meeting_tool(meeting_name: str) -> str:
    """Deletes an entire meeting and all of its associated notes."""
    try:
        conn = sqlite3.connect('backlog.db')
        cursor = conn.cursor()
        # The 'ON DELETE CASCADE' in the table schema handles deleting the notes automatically
        cursor.execute("DELETE FROM meetings WHERE name = ?", (meeting_name,))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return f"Error: No meeting found with name '{meeting_name}'."
        conn.close()
        return f"Successfully deleted the meeting '{meeting_name}' and all its notes."
    except Exception as e:
        return f"Error: Could not delete meeting. {e}"