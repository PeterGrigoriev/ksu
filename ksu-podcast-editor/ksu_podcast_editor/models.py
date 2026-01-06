"""Data models for podcast editing."""

from pydantic import BaseModel


class Word(BaseModel):
    """A word with timestamp information."""

    text: str
    start: float  # Start time in seconds
    end: float  # End time in seconds
    confidence: float = 1.0


class Segment(BaseModel):
    """A segment of audio to be processed."""

    start: float
    end: float
    words: list[Word] = []
    text: str = ""


class EditDecision(BaseModel):
    """A decision about what to edit in the audio."""

    start: float
    end: float
    reason: str  # e.g., "filler", "repetition", "long_pause"
    original_text: str = ""
