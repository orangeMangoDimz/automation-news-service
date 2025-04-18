from google import genai
from google.genai import types
from utils.constant import SUMMARIZE_INSTRUCTION, RESPONSE_NOT_FOUND


class GeminiService:
    def __init__(self, api_key: str) -> None:
        self.client = genai.Client(api_key=api_key)

    def do_get_response(self, contents: str, model: str = "gemini-2.0-flash") -> str:
        response = self.client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SUMMARIZE_INSTRUCTION
            ),
        )

        if response.text is None:
            raise Exception(RESPONSE_NOT_FOUND)

        return response.text
