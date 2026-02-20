import edge_tts
import asyncio
import tempfile
import os
import pygame

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()

# Sweet, natural neural voice — options you can swap:
#   "en-US-JennyNeural"  — warm and friendly (default)
#   "en-US-AriaNeural"   — calm and clear
#   "en-US-SaraNeural"   — bright and polite
VOICE = "en-US-JennyNeural"


async def _generate(text: str, path: str):
    communicate = edge_tts.Communicate(text, voice=VOICE, rate="-5%", pitch="+0Hz")
    await communicate.save(path)


def speak(text: str):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        asyncio.run(_generate(text, tmp_path))
        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(50)
    finally:
        pygame.mixer.music.unload()
        os.unlink(tmp_path)
