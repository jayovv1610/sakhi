# Lighting effects for different moods
MOODS = {
    "happy": "bright",
    "sad": "soft",
    "thinking": "pulse",
    "listening": "glow",
    "idle": "dim",
    "excited": "bright"
}


def status():
    """Show whether Sakhi's lighting system is ready."""

    print("SAKHI lighting ready.")


def set_mood(mood):
    """Choose a lighting effect based on Sakhi's mood."""

    mood = mood.lower()
    effect = MOODS.get(mood, "dim")

    print(f"SAKHI mood: {mood} | lighting effect: {effect}")

