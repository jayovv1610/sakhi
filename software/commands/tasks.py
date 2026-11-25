
import json
import os
import re
from datetime import datetime, timedelta


TASK_FILE = os.path.expanduser("~/SAKHI/data/tasks.json")

NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10
}


def load():
    """Read saved tasks and reminders."""

    if not os.path.exists(TASK_FILE):
        return {"tasks": [], "reminders": []}

    with open(TASK_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save(data):
    """Save tasks without overwriting the original file directly."""

    folder = os.path.dirname(TASK_FILE)
    os.makedirs(folder, exist_ok=True)

    temporary_file = TASK_FILE + ".tmp"

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    os.replace(temporary_file, TASK_FILE)


def read_number(value):
    """Convert a number word or digit into an integer."""

    if value.isdigit():
        return int(value)

    return NUMBER_WORDS.get(value)


def handle_tasks(text):
    """Handle task and reminder commands."""

    text = text.lower().strip()

    # Fix common speech recognition mistakes
    text = re.sub(
        r"^(you mind me|he remind me|you remind me|remind me|mind me) to ",
        "remind me to ",
        text
    )

    data = load()

    # Add a task
    if text.startswith("add task "):
        task = text[len("add task "):].strip()

        if not task:
            return "Please tell me what task to add."

        data["tasks"].append(task)
        save(data)

        return f"Task added: {task}."

    # Show tasks
    if text in ("show my tasks", "show tasks", "list tasks"):
        if not data["tasks"]:
            return "You have no pending tasks."

        tasks = [
            f"Task {number}: {task}"
            for number, task in enumerate(data["tasks"], start=1)
        ]

        return ". ".join(tasks)

    # Complete a task
    if text.startswith("complete task "):
        value = text[len("complete task "):].strip()
        number = read_number(value)

        if number is None or not 1 <= number <= len(data["tasks"]):
            return "I couldn't find that task."

        completed_task = data["tasks"].pop(number - 1)
        save(data)

        return f"Completed task: {completed_task}."

    # Add a reminder
    if text.startswith("remind me to "):
        match = re.fullmatch(
            r"remind me to (.+) in (\w+) (second|minute|hour|day)s?",
            text
        )

        if not match:
            return "Please specify when I should remind you."

        task, amount, unit = match.groups()
        number = read_number(amount)

        if number is None or number <= 0:
            return "I couldn't understand the duration."

        due_time = datetime.now() + timedelta(
            **{unit + "s": number}
        )

        data["reminders"].append({
            "task": task,
            "due": due_time.isoformat()
        })

        save(data)

        unit_name = unit if number == 1 else unit + "s"
        return f"I'll remind you to {task} in {number} {unit_name}."

    # Show reminders
    if text in ("show my reminders", "show reminders"):
        if not data["reminders"]:
            return "You have no pending reminders."

        reminders = []

        for reminder in data["reminders"]:
            due_time = datetime.fromisoformat(reminder["due"])
            formatted_time = due_time.strftime("%d %B, %I:%M %p")

            reminders.append(
                f"{reminder['task']} at {formatted_time}"
            )

        return ". ".join(reminders)

    return None


def due_reminders():
    """Find reminders that are ready to announce."""

    data = load()
    now = datetime.now()

    reminders = []

    for reminder in data["reminders"]:
        due_time = datetime.fromisoformat(reminder["due"])

        if due_time <= now:
            reminders.append(reminder)

    return reminders


def remove_reminder(reminder):
    """Remove a reminder after it has been announced."""

    data = load()

    if reminder in data["reminders"]:
        data["reminders"].remove(reminder)
        save(data)

