
from datetime import datetime


from software.commands.weather import get_weather
from software.commands.news import get_news


def daily_briefing():
    """Give a daily update with the date, time, weather and news."""

    now = datetime.now()

    # Choose a greeting based on the time
    if now.hour < 12:
        greeting = "Good morning!"
    elif now.hour < 17:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"

    # Get today's date and current time
    today = now.strftime("%A, %d %B %Y")
    current_time = now.strftime("%I:%M %p")

    # Get the weather and latest headlines
    weather = get_weather("Hyderabad")
    news = get_news()

    # Put everything together for Sakhi to speak
    briefing = (
        f"{greeting} Today is {today}. "
        f"The time is {current_time}. "
        f"{weather} "
        f"Here are your news updates. {news}"
    )

    return briefing

