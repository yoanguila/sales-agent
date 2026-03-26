from dotenv import load_dotenv
from agent import run_agent

load_dotenv()

print("Sales Agent ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        break
    if not user_input:
        continue

    print("Agent thinking...")
    response = run_agent(user_input)
    print(f"\nAgent: {response}\n")
    