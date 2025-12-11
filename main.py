from src.agent import run

while True:
    prompt = input("👤 ")
    answer = run(prompt)
    print(f"🤖 {answer}")
