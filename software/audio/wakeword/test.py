
import json

import sounddevice as sd
import vosk


MODEL_PATH = "software/audio/models/vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
RECORD_SECONDS = 3

model = vosk.Model(MODEL_PATH)


def detect_wakeword():
    """Listen until someone says Hey Sakhi."""

    print("SAKHI: Waiting for 'Hey Sakhi'...", flush=True)

    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    while True:
        # Record three seconds of microphone audio
        audio = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        # Convert the recorded audio into text
        recognizer.AcceptWaveform(audio.tobytes())

        result = json.loads(recognizer.Result())
        heard_text = result.get("text", "").lower().strip()

        if heard_text:
            print("Heard:", heard_text)

        # Check whether Sakhi's name was spoken
        if "hey sakhi" in heard_text:
            print("SAKHI: Wake word detected!")
            return


if __name__ == "__main__":
    detect_wakeword()
