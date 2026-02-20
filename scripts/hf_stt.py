import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel

# Load model once
model = WhisperModel("base", compute_type="int8")

def listen(fs=16000, silence_threshold=0.015, silence_duration=1.5, max_duration=12):
    """
    Record audio dynamically until silence is detected after speech starts.
    - silence_threshold: RMS amplitude below which audio is considered silent
    - silence_duration:  seconds of silence needed to stop recording
    - max_duration:      hard cap on recording length in seconds
    """
    print("Listening...")

    chunk_size = int(fs * 0.1)          # process in 100ms chunks
    max_chunks = int(max_duration / 0.1)
    silence_chunks_needed = int(silence_duration / 0.1)

    audio_chunks = []
    silent_count = 0
    speech_started = False

    with sd.InputStream(samplerate=fs, channels=1, dtype='float32') as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(chunk_size)
            audio_chunks.append(chunk.copy())

            rms = np.sqrt(np.mean(chunk ** 2))

            if rms > silence_threshold:
                speech_started = True
                silent_count = 0
            elif speech_started:
                silent_count += 1
                if silent_count >= silence_chunks_needed:
                    break

    if not audio_chunks or not speech_started:
        return ""

    recording = np.concatenate(audio_chunks, axis=0)
    # Convert float32 [-1, 1] → int16 for a standard WAV that Whisper handles reliably
    recording_int16 = (recording * 32767).astype(np.int16)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav.write(tmp.name, fs, recording_int16)
        segments, _ = model.transcribe(tmp.name, language="en")

        text = ""
        for segment in segments:
            text += segment.text

    print("You said:", text)
    return text.strip()
