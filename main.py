from src.agent import run


while True:
    prompt = input("👤 ")
    answer = run(prompt)
    print(f"🤖 {answer}")





# from src.utils.telegram import send_and_wait
# reply = send_and_wait(
#     chat_id="228524442",
#     message="How much is 2+2?",
#     timeout=60.0  # Wait up to 60 seconds
# )

# if reply:
#     print(f"User replied: {reply}")
# else:
#     print("No reply received")