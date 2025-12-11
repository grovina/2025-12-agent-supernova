from agents import Agent, Runner, SQLiteSession
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name="Supernova",
    instructions="You are a helpful assistant"
)

session = SQLiteSession("supernova_conversation")

def run(prompt: str) -> str:
    result = Runner.run_sync(agent, prompt, session=session)
    return result.final_output
