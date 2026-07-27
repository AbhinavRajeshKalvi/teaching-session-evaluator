import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

from prompt import SYSTEM_PROMPT
from schema import Evaluation

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def evaluate_transcript(transcript: str):

    prompt = f"""
{SYSTEM_PROMPT}

Transcript:

{transcript}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Evaluation,
            temperature=0
        )
    )

    return response.parsed, response