import os
from dotenv import load_dotenv
from google import genai

from prompt import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

import json

def evaluate_transcript(transcript: str):

    prompt = f"""
{SYSTEM_PROMPT}

Transcript:

{transcript}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text, response