"""
AI Study Buddy - A beginner-friendly chatbot powered by a Large Language Model (LLM).

What it does:
  - Chats with you in the terminal
  - Remembers the conversation (memory)
  - Lets you pick a "mode" (tutor, quiz master, or explainer)
  - Streams answers word-by-word, like ChatGPT/Claude
  - Saves your chat to a file when you're done
"""

import os
import json
from datetime import datetime

from anthropic import Anthropic
from dotenv import load_dotenv

# ---------------------------------------------------------------
# 1. SETUP: load the API key from the .env file
# ---------------------------------------------------------------
load_dotenv()  # reads the .env file and loads ANTHROPIC_API_KEY

if not os.getenv("ANTHROPIC_API_KEY"):
    print("Error: ANTHROPIC_API_KEY not found. Add it to your .env file.")
    raise SystemExit(1)

client = Anthropic()  # automatically uses ANTHROPIC_API_KEY
MODEL = "claude-sonnet-5"

# ---------------------------------------------------------------
# 2. MODES: each mode is a different "system prompt"
#    A system prompt tells the AI how to behave.
# ---------------------------------------------------------------
MODES = {
    "1": {
        "name": "Tutor",
        "prompt": "You are a friendly tutor. Explain topics simply, "
                  "step by step, with a real-life example.",
    },
    "2": {
        "name": "Quiz Master",
        "prompt": "You are a quiz master. Ask the user one question at a time "
                  "about the topic they choose, then tell them if they were right.",
    },
    "3": {
        "name": "Explain Like I'm 5",
        "prompt": "Explain everything as if talking to a 5-year-old. "
                  "Use very simple words and short sentences.",
    },
}


def choose_mode():
    """Ask the user which mode they want and return it."""
    print("\nChoose a mode:")
    for key, mode in MODES.items():
        print(f"  {key}. {mode['name']}")
    choice = input("Enter 1, 2 or 3: ").strip()
    return MODES.get(choice, MODES["1"])  # default to Tutor


def ask_ai(system_prompt, history):
    """Send the whole conversation to the LLM and stream the reply."""
    reply = ""
    with client.messages.stream(
        model=MODEL,
        max_tokens=1000,
        system=system_prompt,
        messages=history,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)  # print word-by-word
            reply += text
    print()
    return reply


def save_chat(mode_name, history):
    """Save the conversation to a JSON file."""
    filename = f"chat_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"mode": mode_name, "messages": history}, f, indent=2)
    print(f"Chat saved to {filename}")


# ---------------------------------------------------------------
# 3. MAIN LOOP: keep chatting until the user types 'quit'
# ---------------------------------------------------------------
def main():
    print("=" * 40)
    print("   Welcome to AI Study Buddy!")
    print("=" * 40)

    mode = choose_mode()
    print(f"\nMode: {mode['name']}. Type 'quit' to exit, 'clear' to reset memory.\n")

    history = []  # this list is the chatbot's "memory"

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "quit":
            if history:
                save_chat(mode["name"], history)
            print("Goodbye! Keep learning!")
            break
        if user_input.lower() == "clear":
            history = []
            print("Memory cleared.\n")
            continue

        # Add the user's message to memory
        history.append({"role": "user", "content": user_input})

        print("Buddy: ", end="")
        try:
            reply = ask_ai(mode["prompt"], history)
            # Add the AI's reply to memory so it remembers next time
            history.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"\nSomething went wrong: {e}")
            history.pop()  # remove the message that failed
        print()


if __name__ == "__main__":
    main()
