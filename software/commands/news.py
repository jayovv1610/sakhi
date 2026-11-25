
import requests
import xml.etree.ElementTree as ET


def get_news():
    """Get the latest three headlines from Google News."""

    news_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"

    try:
        # Get the latest news from Google
        response = requests.get(news_url, timeout=15)
        response.raise_for_status()

        # Read the RSS feed
        news_feed = ET.fromstring(response.content)

        headlines = []

        # Pick the first three headlines
        for article in news_feed.findall("./channel/item")[:3]:
            title = article.findtext("title")

            if title:
                headlines.append(title)

        if not headlines:
            return "No news headlines available right now."

        return ". ".join(headlines)

    except (requests.RequestException, ET.ParseError):
        return "I couldn't retrieve the latest news right now."
