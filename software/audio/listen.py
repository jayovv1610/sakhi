
import json
import queue

import sounddevice as sd
import vosk

from software.commands.tasks import due_reminders


# Microphone and speech recognition settings
MODEL_PATH = "software/audio/models/vosk-model-small-en-us-0.15"
MICROPHONE = "Plantronics Blackwire"
SAMPLE_RATE = 16000

# Load the speech recognition model once
model = vosk.Model(MODEL_PATH)

audio_queue = queue.Queue()


def callback(indata, frames, time_info, status):
    """Collect audio from the microphone."""

    if status:
        print("Microphone status:", status)

    audio_queue.put(bytes(indata))


def listen():
    """Listen until Sakhi hears a complete sentence."""

    print("SAKHI: Listening...", flush=True)

    # Clear audio left over from the previous conversation
    while not audio_queue.empty():
        try:
            audio_queue.get_nowait()
        except queue.Empty:
            break

    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=4000,
            device=MICROPHONE,
            channels=1,
            dtype="int16",
            callback=callback
        ):
            while True:

                # Let the main program handle due reminders
                if due_reminders():
                    return "__reminder_due__"

                try:
                    audio = audio_queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                # Vosk returns True when it detects a full phrase
                if not recognizer.AcceptWaveform(audio):
                    continue

                result = json.loads(recognizer.Result())
                message = result.get("text", "").strip()

                if message:
                    print("You:", message, flush=True)
                    return message

    except Exception as error:
        print("Microphone error:", error, flush=True)
        raise


if __name__ == "__main__":
    listen()
