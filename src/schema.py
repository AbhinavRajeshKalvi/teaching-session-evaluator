from typing import List
from pydantic import BaseModel, Field


class Evaluation(BaseModel):
    """
    Structured evaluation returned by the LLM.
    """

    engagement_score: int = Field(
        ge=1,
        le=10,
        description="Student engagement score from 1 to 10."
    )

    clarity_score: int = Field(
        ge=1,
        le=10,
        description="Teacher clarity score from 1 to 10."
    )

    pacing_score: int = Field(
        ge=1,
        le=10,
        description="Lesson pacing score from 1 to 10."
    )

    engagement_indicators: List[str] = Field(
        min_length=1,
        description="Observable signs of student engagement."
    )

    notable_moments: List[str] = Field(
        min_length=1,
        description="Important teaching or learning moments."
    )

    summary: str = Field(
        min_length=20,
        description="A concise summary of the tutoring session."
    )