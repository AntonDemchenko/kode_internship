from base_app.utils.json import Json


class SpeechRecognition(Json):
    def post(self, request):
        return {
            "text": "Hello"
        }
