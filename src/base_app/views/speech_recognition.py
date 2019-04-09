import rmr
from settings import SPEECH_RECOGNITION

from base_app.utils.json import Json
from base_app.integrations.speech_recognition import speech_to_text


class SpeechRecognition(Json):
    max_size = SPEECH_RECOGNITION["FILE_MAX_SIZE"]

    def post(self, request):
        audio = request.FILES.get("audio")

        if not audio:
            raise rmr.ClientError("Please provide audio file.", code=400)

        if audio.size > self.max_size:
            raise rmr.ClientError(
                "Please provide smaller file. "
                "Maximal possible size is {} byte(s)".format(self.max_size),
                code=400
            )

        try:
            text = speech_to_text(audio)
        except RuntimeError:
            raise rmr.ServerError(
                "Something went wrong. Please try again later.",
                code=500
            )

        if not text:
            raise rmr.ClientError(
                "Unable to recognize speech. "
                "Please provide another audio file.",
                code=400
            )

        return {
            "text": text
        }
