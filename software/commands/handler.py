
from datetime import datetime

from software.commands.web import search_web
from software.commands.tasks import handle_tasks
from software.commands.briefing import daily_briefing
from software.commands.weather import get_weather


def handle_command(text):
    """Check whether Sakhi can handle a request directly."""

    text = text.lower().strip().rstrip("?!.,")
    text = text.replace("'", "")

    # Help
    if text in (
        "help",
        "what can you do",
        "what are your capabilities"
    ):
        return (
            "I can tell you the time and date, check the weather, "
            "search the web, manage reminders, give daily briefings, "
            "and answer questions."
        )

    # Time
    if text in (
        "what time is it",
        "tell me the time",
        "current time",
        "time"
    ):
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}."

    # Date
    if text in (
        "what days it",
        "what day is today",
        "what day is it",
        "what is the date",
        "what is todays date",
        "todays date",
        "what day is it today",
        "today"
    ):
        today = datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {today}."

    # Weather
    if "weather" in text or "temperature" in text:
        if " in " in text:
            city = text.split(" in ", 1)[1]
        else:
            city = "Hyderabad"

        return get_weather(city)

    # Web search
    search_phrases = (
        "search for ",
        "search the web for ",
        "look up ",
        "search online for "
    )

    for phrase in search_phrases:
        if text.startswith(phrase):
            search_query = text[len(phrase):]
            return search_web(search_query)

    # Morning briefing
    if text in (
        "good morning",
        "daily briefing",
        "give me my daily briefing",
        "give me my briefing"
    ):
        return daily_briefing()

    # Reminders and tasks
    task_response = handle_tasks(text)

    if task_response:
        return task_response

    # Let the AI handle normal conversation
    return None

