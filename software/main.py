
import logging
import time

from software.ai.brain import think
from software.audio.listen import listen
from software.audio.voice import speak
from software.commands.handler import handle_command
from software.commands.tasks import due_reminders, remove_reminder
from software.core.logger import setup_logger
from software.core.state import SakhiState, set_state


logger = setup_logger()


def check_reminders():
    """Read out reminders that are due."""

    for reminder in due_reminders():
        set_state(SakhiState.SPEAKING)

        interrupted_message = speak("Reminder: " + reminder["task"])

        if interrupted_message:
            return interrupted_message

        remove_reminder(reminder)

    return None


def get_response(message):
    """Check for a command before asking the AI."""

    command_reply = handle_command(message)

    if command_reply:
        return command_reply

    return think(message)


def main():
    print("SAKHI is online.")
    print("Talk normally. Say exit to shut down.")

    logger.info("SAKHI controller started")

    pending_message = None

    while True:
        try:
            set_state(SakhiState.LISTENING)

            if pending_message:
                message = pending_message
                pending_message = None
            else:
                message = listen()

            # The listener uses this to signal a due reminder.
            if message == "__reminder_due__":
                pending_message = check_reminders()
                set_state(SakhiState.IDLE)
                continue

            if not message or not message.strip():
                set_state(SakhiState.IDLE)
                continue

            message = message.strip()
            logger.info("Input received: %s", message)

            if message.lower() == "exit":
                set_state(SakhiState.SPEAKING)
                speak("Shutting down.")

                logger.info("Shutdown requested")
                set_state(SakhiState.IDLE)
                break

            set_state(SakhiState.THINKING)
            response = get_response(message)

            print("SAKHI:", response)

            set_state(SakhiState.SPEAKING)
            pending_message = speak(response)

            set_state(SakhiState.IDLE)

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            set_state(SakhiState.IDLE)
            break

        except Exception:
            logger.exception("Controller runtime error")
            print("SAKHI ERROR: Something went wrong. Check logs.")

            try:
                set_state(SakhiState.ERROR)
                speak("I encountered an error. I'll recover.")
            except Exception:
                logger.exception("Error recovery failed")

            set_state(SakhiState.IDLE)
            time.sleep(2)


if __name__ == "__main__":
    main()
