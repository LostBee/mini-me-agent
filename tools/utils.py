# tools/utils.py

from datetime import date
from langchain.tools import tool

@tool
def get_todays_date_tool() -> str:
    """Returns today's date in YYYY-MM-DD format."""
    return date.today().isoformat()