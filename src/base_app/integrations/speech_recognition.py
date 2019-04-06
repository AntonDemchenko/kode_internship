import base64


def speech_to_text(audio: bytes) -> str:
    audio = base64.b64encode(audio)
    return "Hello"
