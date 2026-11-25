
import json
import os
import queue
import subprocess
import tempfile

import sounddevice as sd
import vosk

from software.audio import listen as microphone


# Voice and speaker settings
VOICE_MODEL = os.path.expanduser(
    "~/SAKHI/software/audio/voices/voice.onnx"
)

PIPER = os.path.expanduser("~/SAKHI/.venv/bin/piper")
SPEAKER = "plughw:2,0"


def speak(text):
    """Make Sakhi speak and listen for interruptions."""

    if not text or not text.strip():
        return None

    # Create a temporary file for the generated speech
    with tempfile.NamedTemporaryFile(
        suffix=".wav", delete=False
    ) as file:
        audio_file = file.name

    player = None
    audio_queue = queue.Queue()

    def record_audio(indata, frames, time_info, status):
        if status:
            print("Microphone status:", status)

        audio_queue.put(bytes(indata))

    try:
        # Convert text into speech using Piper
        subprocess.run(
            [
                PIPER,
                "--model", VOICE_MODEL,
                "--output_file", audio_file
            ],
            input=text,
            text=True,
            check=True,
            timeout=60
        )

        # Listen while Sakhi is speaking
        recognizer = vosk.KaldiRecognizer(
            microphone.model,
            microphone.SAMPLE_RATE
        )

        mic_device = getattr(
            microphone,
            "MICROPHONE",
            getattr(microphone, "DEVICE", None)
        )

        with sd.RawInputStream(
            samplerate=microphone.SAMPLE_RATE,
            blocksize=4000,
            device=mic_device,
            channels=1,
            dtype="int16",
            callback=record_audio
        ):
            player = subprocess.Popen(
                ["aplay", "-D", SPEAKER, audio_file]
            )

            while player.poll() is None:
                try:
                    audio = audio_queue.get(timeout=0.2)
                except queue.Empty:
                    continue

                if recognizer.AcceptWaveform(audio):
                    result = json.loads(recognizer.Result())
                    message = result.get("text", "").strip()

                    if message:
                        print("SAKHI: Interrupted!", flush=True)

                        player.terminate()
                        player.wait(timeout=3)

                        return message

            if player.returncode != 0:
                raise RuntimeError("Audio playback failed")

        return None

    finally:
        # Stop playback if it is still running
        if player is not None and player.poll() is None:
            player.kill()
            player.wait()

        # Remove the temporary audio file
        if os.path.exists(audio_file):
            os.remove(audio_file)
