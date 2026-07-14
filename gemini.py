
from google import genai
from config import Config


class GeminiChat:
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model = "gemini-2.5-flash"

    def generate_response(self, messages):
        """
        messages example:
        [
            {"role":"user","content":"Hello"},
            {"role":"assistant","content":"Hi!"}
        ]
        """

        try:
            contents = []

            for message in messages:
                role = "user" if message["role"] == "user" else "model"

                contents.append({
                    "role": role,
                    "parts": [
                        {"text": message["content"]}
                    ]
                })

            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )

            return response.text

        except Exception as e:
            print(e)
            return "Something went wrong while contacting Gemini."
