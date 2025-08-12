# main.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool

# --- 1. Tool Definition ---
# We can now go back to our clean, flattened tool definition.
# The new agent type handles this structure reliably.
@tool
def score_rice_tool(name: str, reach: int, impact: float, confidence: float, effort: float) -> str:
    """
    Calculates the RICE score for a given backlog item.
    Use this tool when you need to prioritize a feature or backlog item.
    """
    if effort == 0:
        return "Error: Effort cannot be zero."

    rice_score = (reach * impact * confidence) / effort
    
    return (
        f"The RICE score for '{name}' is {rice_score:.2f}. "
        f"Breakdown: [Reach: {reach}, Impact: {impact}, "
        f"Confidence: {confidence}, Effort: {effort}]"
    )

# --- 2. Agent Setup ---
def main():
    load_dotenv()
    # Note: Using your specified model name.
    # Ensure your API key has access to this model.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    tools = [score_rice_tool]

    # This is a more modern way to create the agent's prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful product manager assistant."),
        ("human", "{input}"),
        # This placeholder is where the agent stores conversation history and tool outputs
        ("placeholder", "{agent_scratchpad}"),
    ])

    # Create the modern tool-calling agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # The AgentExecutor remains the same
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    user_request = (
        "Please prioritize this feature: 'Users want to log in with Google'. "
        "I estimate the reach is 2000 users, impact is 3, confidence is 0.8, "
        "and effort is 3 person-months."
    )
    
    # Use .invoke() which is the standard way to run chains/agents
    result = agent_executor.invoke({"input": user_request})
    
    print("\n--- Final Answer ---")
    print(result['output'])

if __name__ == "__main__":
    main()