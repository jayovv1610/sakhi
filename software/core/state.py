
from enum import Enum


class SakhiState(Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    SPEAKING = "SPEAKING"
    ERROR = "ERROR"


# Sakhi starts in the idle state
_current_state = SakhiState.IDLE


def set_state(new_state):
    """Change Sakhi's current state."""

    global _current_state

    if not isinstance(new_state, SakhiState):
        raise ValueError("Invalid SAKHI state")

    # Only update the state if it has changed
    if new_state != _current_state:
        print(f"[STATE] {_current_state.value} -> {new_state.value}")
        _current_state = new_state


def get_state():
    """Return Sakhi's current state."""

    return _current_state


# Run a quick test when this file is opened directly
if __name__ == "__main__":
    print("Current state:", get_state().value)

    set_state(SakhiState.LISTENING)
    set_state(SakhiState.THINKING)
    set_state(SakhiState.SPEAKING)
    set_state(SakhiState.IDLE)

