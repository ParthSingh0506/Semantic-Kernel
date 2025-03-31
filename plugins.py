import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

# Step 1: Define a Simple Plugin (Function) for Weather Updates
def weather_plugin(location: str) -> str:
    # Simulating a weather API response
    weather_data = {
        "New York": "Sunny, 25°C",
        "London": "Cloudy, 18°C",
        "Tokyo": "Rainy, 22°C"
    }
    return weather_data.get(location, "Weather data not available.")

# Step 2: Initialize Semantic Kernel
kernel = sk.Kernel()
kernel.add_service("openai-chat", OpenAIChatCompletion(model="gpt-4", api_key="your-api-key"))

# Step 3: Register the Plugin (Function) in Semantic Kernel
kernel.add_plugin("WeatherPlugin", weather_plugin)

# Step 4: Calling the Plugin through Semantic Kernel
location = "New York"
response = kernel.invoke("WeatherPlugin", location)
print(f"Weather in {location}: {response}")
