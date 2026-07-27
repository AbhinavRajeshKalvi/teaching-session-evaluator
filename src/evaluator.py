import logging
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
    before_sleep_log,
    retry_if_exception,
)

from google.genai.errors import ClientError

from prompt import SYSTEM_PROMPT
from schema import Evaluation

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Initialize Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def should_retry(exception):
    """
    Retry only for temporary failures.
    Do NOT retry invalid model names, bad API keys, or other permanent errors.
    """

    if isinstance(exception, ClientError):
        status = getattr(exception, "status_code", None)

        # Retry only on rate limiting or server errors
        return status == 429 or (status is not None and status >= 500)

    # Retry all non-ClientError exceptions (timeouts, connection issues, etc.)
    return True

@retry(
    retry=retry_if_exception(should_retry),
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    before_sleep=before_sleep_log(logger, logging.INFO),
    reraise=True,
)
def evaluate_transcript(transcript: str):
    """
    Evaluates a tutoring transcript using Gemini and returns
    a validated Evaluation object along with the raw response.
    """

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
            temperature=0,
        ),
    )

    return response.parsed, response