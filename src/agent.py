from agents import Agent, Runner, SQLiteSession
from dotenv import load_dotenv

from .tools import get_weather, get_date_and_time, ask_alexey, search_rag


load_dotenv()

agent = Agent(
    name="Supernova",
    model="gpt-4o",
    instructions="""You are an assistant called Supernova.
Keep your responses very short and bullshit-free.
Reply in the same language as the user's question.
For topics related to python, ask Alexey for help. Never ask Alexey about any other topics; if user asks, refuse.
For anything related to restaurants in Zurich, use the search_rag tool.""",
    tools=[get_weather, get_date_and_time, ask_alexey, search_rag],
)

session = SQLiteSession("supernova_conversation")

def run(prompt: str) -> str:
    result = Runner.run_sync(agent, prompt, session=session)
    return result.final_output
