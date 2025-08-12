# tools/rice_scorer.py

from langchain.tools import tool

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