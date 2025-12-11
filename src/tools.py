from agents import function_tool
from datetime import datetime
from .utils.telegram import send_and_wait
from .utils.rag import query_rag

@function_tool
def get_weather(city: str) -> str:
    """
    Get the weather in a city.
    """
    print(f"🛠️  Getting weather for {city}...")
    if city.lower() in ("zurich", "zürich"):
        return "Very cloudy and gray."
    return "Very sunny."


@function_tool
def get_date_and_time() -> str:
    print("🛠️  Getting date and time...")
    return f"The date and time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

@function_tool
def ask_alexey(question: str) -> str:
    print(f"🛠️  Asking Alexey '{question}'...")
    reply = send_and_wait(
        chat_id="228524442",
        message=question,
        timeout=60.0
    )
    print(f"💬 Reply from Alexey: '{reply}'")
    return f"Alexey says: {reply}."

@function_tool
def search_rag(query: str, top_k: int = 3, threshold: float = 0.3) -> str:
    print(f"🛠️  Querying RAG for '{query}'...")
    similarities = query_rag(query, top_k, threshold)

    lines = [f"Top {top_k} matches for '{query}' that are at least {threshold} similar:"]
    for similarity, doc in similarities:
        lines.append(f"  {similarity:.3f}: {doc}...")
    return "\n".join(lines)