# main.py
# Setting up API and hitting LLM for response
# langchain reference doc: https://python.langchain.com/docs/integrations/chat/google_generative_ai/

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain

# Load environment variables from .env file
load_dotenv()

# Initialize the LLM
# This creates an object that connects to the Gemini model.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Create a conversation chain using laangchain
# This chain automatically includes a simple memory module
conversation = ConversationChain(llm=llm, verbose=True) #We can see the full prompt with verbose

# Let's have a conversation
# We use .invoke() on the chain now, passing the input in a dictionary.result = llm.invoke("Explain what a Product Manager does in one sentence.")
response1 = conversation.invoke({"input": "Hi, I'm a Product Manager for an AI Companion Site."})
print("AI Response 1:", response1['response'])

print("\n" + "="*20 + "\n") # Adding a separator for clarity

response2 = conversation.invoke({"input": "What kind of company did I say I work for?"})
print("AI Response 2:", response2['response'])