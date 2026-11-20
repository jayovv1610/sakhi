from software.ai.brain import think
from software.audio.voice import speak
from software.audio.listen import listen
from software.commands.handler import handle_command
from software.core.state import SakhiState, set_state


def main():
    print("SAKHI is online.")
    print("Talk normally. Say exit to shut down.")

    while True:
        try:
            set_state(SakhiState.LISTENING)
            message = listen()

            if not message or not message.strip():
                set_state(SakhiState.IDLE)
                continue

            if message.lower().strip() == "exit":
                set_state(SakhiState.SPEAKING)
                speak("Shutting down.")
                set_state(SakhiState.IDLE)
                break

            set_state(SakhiState.THINKING)
            command_response = handle_command(message)

            if command_response:
                response = command_response
            else:
                response = think(message)

            print("SAKHI:", response)

            set_state(SakhiState.SPEAKING)
            speak(response)
            set_state(SakhiState.IDLE)

        except KeyboardInterrupt:
            set_state(SakhiState.IDLE)
            break

        except Exception as e:
            print("SAKHI ERROR:", e)
            set_state(SakhiState.ERROR)
            set_state(SakhiState.IDLE)


if __name__ == "__main__":
    main()
