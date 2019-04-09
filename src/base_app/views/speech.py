from rest_framework.views import APIView
from rest_framework.response import Response
from mutagen.flac import FLAC
from mutagen import MutagenError

from base_app.external.speech import speech_to_text
from django.conf import settings


class SpeechRecognition(APIView):
    MAX_SIZE = settings.SPEECH["MAX_SIZE"]
    MAX_LENGTH = settings.SPEECH["MAX_LENGTH"]

    @staticmethod
    def error(message, status_code):
        return Response(
            {"error": message},
            status_code
        )

    @staticmethod
    def get_flac(audio):
        flac = None
        try:
            flac = FLAC(audio)
        except MutagenError:
            pass
        finally:
            audio.seek(0)
        return flac

    def post(self, request):
        audio = request.FILES.get("audio")

        if not audio:
            return self.error("Please provide audio file.", 400)

        if audio.size > self.MAX_SIZE:
            return self.error(
                "Please provide smaller file. "
                "Maximal possible size is {} byte(s).".format(self.MAX_SIZE),
                400
            )

        flac = self.get_flac(audio)
        if not flac:
            return self.error("Please provide audio file in FLAC encoding.", 400)

        if flac.info.length > self.MAX_LENGTH:
            return self.error(
                "Please provide shorter audio file. "
                "Maximal possible length is {} second(s).".format(self.MAX_LENGTH),
                400
            )

        if flac.info.channels != 1:
            return self.error(
                "Passed stereo file. "
                "Please provide one channel audio file.",
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
            "result": text
        })
