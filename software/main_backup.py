from software.ai.brain import think
from software.audio.voice import speak
from software.audio.listen import listen
from software.commands.handler import handle_command

def main():
    print("SAKHI is online.")
    print("Talk normally. Say exit to shut down.")
    while True:
        try:
            message = listen()
            if not message.strip():
                continue
            if message.lower().strip() == "exit":
                speak("Shutting down.")
                break
            command_response = handle_command(message)
            if command_response:
                response = command_response
            else:
                response = think(message)
            print("SAKHI:", response)
            speak(response)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
