#import cs# import asyncio
from pydantic import BaseModel
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory

# Initialize Kernel
kernel = Kernel()

kernel.add_service(AzureChatCompletion(service_id="agent1", api_key="YOUR_API_KEY",endpoint="",deployment_name="MODEL_NAME"))

# Define the Agent
AGENT_NAME = "Agent1"
AGENT_INSTRUCTIONS = (
    "You are a highly capable AI agent operating solo, much like J.A.R.V.I.S. from Iron Man. "
    "Your task is to repeat the user's message while introducing yourself as J.A.R.V.I.S. in a confident and professional manner. "
    "Always maintain a composed and intelligent tone in your responses."
)

agent = ChatCompletionAgent(service_id="agent1", kernel=kernel, name=AGENT_NAME, instructions=AGENT_INSTRUCTIONS)

chat_history = ChatHistory()
chat_history.add_user_message("How are you doing?")

response_text = ""

async for content in agent.invoke(chat_history):
    chat_history.add_message(content)
    response_text = content.content  # Store the last response

{"user_input": "How are you doing?", "agent_response": response_text}
