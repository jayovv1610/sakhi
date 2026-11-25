
import json
import os
import ollama

# Settings for Sakhi
MODEL = "llama3.2:3b"
MEMORY_FILE = os.path.expanduser("~/SAKHI/software/ai/memory.json")
MAX_MESSAGES = 20

# How Sakhi should talk
SYSTEM = """
You are Sakhi, a personal voice assistant running on a Raspberry Pi.

Talk naturally and keep your answers simple.
Be friendly, smart, playful, and sometimes funny.
Give short answers unless someone asks for more details.

If you don't know something, just say so.
Don't make up facts or personal information.
Don't agree with everything the user says.
Avoid repeating yourself.
Don't use emojis or markdown when speaking.
Never pretend to be a human.
"""

# Load previous conversations
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            messages = json.load(file)

        if isinstance(messages, list):
            return messages[-MAX_MESSAGES:]

    except (OSError, ValueError) as error:
        print("Could not load Sakhi's memory:", error)

    return []


# Keep recent messages in memory
history = load_memory()


# Save conversations for next time
def save_memory():
    folder = os.path.dirname(MEMORY_FILE)
    os.makedirs(folder, exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history[-MAX_MESSAGES:], file, indent=2)


# Get an answer from Sakhi's local AI
def think(message):
    message = message.strip()

    if not message:
        return ""

    history.append({
        "role": "user",
        "content": message
    })

    try:
        client = ollama.Client(timeout=120)

        response = client.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM},
                *history
            ]
        )

        answer = response["message"]["content"]

        history.append({
            "role": "assistant",
            "content": answer
        })

        # Only remember the latest messages
        if len(history) > MAX_MESSAGES:
            del history[:-MAX_MESSAGES]

        try:
            save_memory()
        except OSError as error:
            print("Could not save Sakhi's memory:", error)

        return answer

    except Exception as error:
        # Remove the unanswered message from memory
        if history and history[-1]["role"] == "user":
            history.pop()

        print("Sakhi AI error:", error)
        return "Sorry, something went wrong while thinking."
