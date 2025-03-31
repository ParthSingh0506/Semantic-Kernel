import asyncio
from pydantic import BaseModel
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory

# Initialize Kernel
kernel = Kernel()

# Add multiple services for different agents
kernel.add_service(AzureChatCompletion(service_id="banking_agent", api_key="YOUR_API_KEY", endpoint="", deployment_name="MODEL_NAME"))
kernel.add_service(AzureChatCompletion(service_id="healthcare_agent", api_key="YOUR_API_KEY", endpoint="", deployment_name="MODEL_NAME"))
kernel.add_service(AzureChatCompletion(service_id="classifier_agent", api_key="YOUR_API_KEY", endpoint="", deployment_name="MODEL_NAME"))

# Define Orchestrator Agent
CLASSIFIER_AGENT = ChatCompletionAgent(
    service_id="orchestrator_agent", kernel=kernel, name="OrchestratorAgent",
    instructions="You are an AI responsible for classifying user queries. Identify whether the query belongs to banking or healthcare. Respond with either 'banking' or 'healthcare'."
)

# Define Domain-Specific Agents
BANKING_AGENT = ChatCompletionAgent(
    service_id="banking_agent", kernel=kernel, name="BankingAgent",
    instructions="You are an AI specializing in banking queries. Answer user queries related to finance and banking."
)

HEALTHCARE_AGENT = ChatCompletionAgent(
    service_id="healthcare_agent", kernel=kernel, name="HealthcareAgent",
    instructions="You are an AI specializing in healthcare queries. Answer user queries related to medical and health topics."
)

# Function to Determine the Appropriate Agent
async def identify_agent(user_input: str):
    chat_history = ChatHistory()
    chat_history.add_user_message(user_input)
    async for content in CLASSIFIER_AGENT.invoke(chat_history):
        classification = content.content.lower()
        if "banking" in classification:
            return BANKING_AGENT
        elif "healthcare" in classification:
            return HEALTHCARE_AGENT
    return None

# Function to Handle User Query
async def handle_query(user_input: str):
    selected_agent = await identify_agent(user_input)
    if not selected_agent:
        return {"error": "No suitable agent found for the query."}
    
    chat_history = ChatHistory()
    chat_history.add_user_message(user_input)
    response_text = ""
    async for content in selected_agent.invoke(chat_history):
        chat_history.add_message(content)
        response_text = content.content
    
    return {"user_input": user_input, "agent_response": response_text}

# Example Usage
user_query = "What are the best practices for securing a bank account?"
response = asyncio.run(handle_query(user_query))
print(response)
