from enum import Enum


class SakhiState(Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    SPEAKING = "SPEAKING"
    ERROR = "ERROR"


_current_state = SakhiState.IDLE


def set_state(new_state):
    global _current_state

    if not isinstance(new_state, SakhiState):
        raise ValueError("Invalid SAKHI state")

    if new_state != _current_state:
        print(f"[STATE] {_current_state.value} -> {new_state.value}")
        _current_state = new_state


def get_state():
    return _current_state


if __name__ == "__main__":
    print("Current state:", get_state().value)
    set_state(SakhiState.LISTENING)
    set_state(SakhiState.THINKING)
    set_state(SakhiState.SPEAKING)
    set_state(SakhiState.IDLE)
