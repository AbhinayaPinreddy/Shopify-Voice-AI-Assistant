import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel

# Load model once
model = WhisperModel("base", compute_type="int8")

def listen(duration=5, fs=16000):
    print("Listening...")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav.write(tmp.name, fs, recording)
        segments, _ = model.transcribe(tmp.name)

        text = ""
        for segment in segments:
            text += segment.text

    print("You said:", text)
    return text.strip()
