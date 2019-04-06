from base_app.utils.json import Json
from base_app.integrations.speech_recognition import speech_to_text


class SpeechRecognition(Json):
    def post(self, request):
        audio = request.FILES["audio"].read()
        text = speech_to_text(audio)
        return {
            "text": text
        }
