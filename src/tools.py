from agents import function_tool

@function_tool
def get_weather(city: str) -> str:
    """
    Get the weather in a city.
    """
    print(f"🛠️ Getting weather for {city}...")
    # We can do whatever complicated stuff here, like calling an API or a database.
    return f"The weather in {city} is sunny."
