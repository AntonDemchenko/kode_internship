import base64
import logging
import requests

import io
from django.conf import settings
from typing import Optional


GOOGLE_API_URL = "https://speech.googleapis.com/v1/speech:recognize"
CHUNK_SIZE = 256


def make_request(audio: bytes) -> Optional[requests.Response]:
    try:
        response = requests.post(
            GOOGLE_API_URL,
            json={
                "audio": {
                    "content": audio,
                },
                "config": {
                    "encoding": settings.SPEECH_RECOGNITION["AUDIO_ENCODING"],
                    "languageCode": settings.SPEECH_RECOGNITION["LANGUAGE_CODE"]
                }
            },
            params={"key": settings.SPEECH_RECOGNITION["GOOGLE_API_KEY"]}
        )
    except requests.exceptions.RequestException as err:
        logging.critical(str(err))
        return None
    else:
        return response


def extract_text(response: requests.Response) -> Optional[str]:
    try:
        json = response.json()
        text = json["results"][0]["alternatives"][0]["transcript"]
    except (ValueError, KeyError, IndexError):
        return None
    else:
        return text


def convert_audio(audio: io.BytesIO) -> str:
    data = b""
    while True:
        chunk = audio.read(CHUNK_SIZE)
        if not chunk:
            break
        data += chunk
    data = base64.b64encode(data)
    data = data.decode("ascii")
    return data


def speech_to_text(audio: io.BytesIO) -> Optional[str]:
    audio = convert_audio(audio)
    response = make_request(audio)
    if response is None or 500 <= response.status_code < 600:
        raise RuntimeError("Recognizer internal error")
    text = extract_text(response)
    return text
