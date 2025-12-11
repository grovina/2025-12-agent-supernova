from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name="Supernova",
    instructions="You are a helpful assistant"
)

def run(prompt: str) -> str:
    result = Runner.run_sync(agent, prompt)
    return result.final_output
