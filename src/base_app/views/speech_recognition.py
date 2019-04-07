import rmr

from base_app.utils.json import Json
from base_app.integrations.speech_recognition import speech_to_text


class SpeechRecognition(Json):
    def post(self, request):
        audio = request.FILES.get("audio")
        if not audio:
            raise rmr.ClientError("Please provide audio file.", code=400)
        audio = audio.read()
        text = speech_to_text(audio)
        if not text:
            raise rmr.ClientError(
                "Unable to recognize speech. "
                "Please provide another audio file.",
                code=400
            )
        return {
            "text": text
        }
