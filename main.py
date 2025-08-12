# main.py
# Setting up API and hitting LLM for response

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# 1. Initialize the LLM
# This creates an object that connects to the Gemini model.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 2. Invoke the LLM
# We send our first prompt to the model.
result = llm.invoke("Explain what a Product Manager does in one sentence.")

# 3. Print the result
# The response from the LLM is stored in the 'content' attribute.
print(result.content)