from enum import Enum
from pathlib import Path


class SakhiState(Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    SPEAKING = "SPEAKING"
    ERROR = "ERROR"


_current_state = SakhiState.IDLE
state_file = Path(__file__).resolve().parents[2] / "data" / "eye_state.txt"


def set_state(new_state):
    global _current_state

    if not isinstance(new_state, SakhiState):
        raise ValueError("Invalid SAKHI state")

    if new_state == _current_state:
        return

    print(f"[STATE] {_current_state.value} -> {new_state.value}")
    _current_state = new_state

    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(new_state.value)


def get_state():
    return _current_state
