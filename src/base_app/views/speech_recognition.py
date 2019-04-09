from settings import SPEECH_RECOGNITION

from rest_framework.views import APIView
from rest_framework.response import Response
from base_app.integrations.speech_recognition import speech_to_text


class SpeechRecognition(APIView):
    max_size = SPEECH_RECOGNITION["FILE_MAX_SIZE"]

    @staticmethod
    def error(message, status_code):
        return Response(
            {"error": message},
            status_code
        )

    def post(self, request):
        audio = request.FILES.get("audio")

        if not audio:
            return self.error("Please provide audio file.", 400)

        if audio.size > self.max_size:
            return self.error(
                "Please provide smaller file. "
                "Maximal possible size is {} byte(s)".format(self.max_size),
                400
            )

        try:
            text = speech_to_text(audio)
        except RuntimeError:
            return self.error(
                "Something went wrong. Please try again later.",
                500
            )

        if not text:
            return self.error(
                "Unable to recognize speech. "
                "Please provide another audio file.",
                400
            )

        return Response({
            "text": text
        })
