import base64
import logging
import requests

from settings import SPEECH_RECOGNITION


def make_request(audio: bytes) -> requests.Response:
    try:
        response = requests.post(
            "https://speech.googleapis.com/v1/speech:recognize",
            json={
                "audio": {
                    "content": audio,
                },
                "config": {
                    "encoding": SPEECH_RECOGNITION["AUDIO_ENCODING"],
                    "languageCode": SPEECH_RECOGNITION["LANGUAGE_CODE"]
                }
            },
            params={"key": SPEECH_RECOGNITION["GOOGLE_API_KEY"]}
        )
    except requests.exceptions.RequestException as err:
        logging.critical(repr(err))
        return None
    else:
        return response


def extract_text(response: requests.Response) -> str:
    try:
        json = response.json()
        text = json["results"][0]["alternatives"][0]["transcript"]
    except (ValueError, KeyError, IndexError):
        return None
    else:
        return text


def speech_to_text(audio: bytes) -> str:
    audio = base64.b64encode(audio)
    audio = audio.decode("ascii")
    response = make_request(audio)
    if not response:
        raise RuntimeError
    text = extract_text(response)
    return text
