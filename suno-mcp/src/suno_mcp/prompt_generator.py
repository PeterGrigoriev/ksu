"""Generate Suno prompts from conversation analysis."""

from pydantic import BaseModel


class ConversationAnalysis(BaseModel):
    """Analysis results from a client conversation."""

    mood: str
    themes: list[str]
    emotions: list[str]
    suggested_genres: list[str]
    key_phrases: list[str]
    energy_level: str  # low, medium, high
    summary: str


class SunoPrompt(BaseModel):
    """A prompt suitable for Suno API."""

    prompt: str
    style: str | None = None
    title: str | None = None
    instrumental: bool = False


def analyze_conversation(conversation: str) -> ConversationAnalysis:
    """
    Analyze a conversation to extract musical elements.

    This is a placeholder - in practice, the LLM (Claude) will do the analysis
    and call this to structure the results.
    """
    # Default analysis - Claude will provide actual values via tool calls
    return ConversationAnalysis(
        mood="neutral",
        themes=["conversation"],
        emotions=["calm"],
        suggested_genres=["ambient"],
        key_phrases=[],
        energy_level="medium",
        summary="A conversation between client and service provider."
    )


def generate_prompt(
    analysis: ConversationAnalysis | None = None,
    mood: str | None = None,
    themes: list[str] | None = None,
    style: str | None = None,
    instrumental: bool = False,
) -> SunoPrompt:
    """
    Generate a Suno-compatible prompt from analysis or direct parameters.
    """
    if analysis:
        mood = mood or analysis.mood
        themes = themes or analysis.themes
        style = style or (analysis.suggested_genres[0] if analysis.suggested_genres else None)

    # Build prompt parts
    parts = []

    if mood:
        parts.append(f"{mood} mood")

    if themes:
        parts.append(", ".join(themes[:3]))  # Limit to 3 themes

    if style:
        parts.append(f"{style} style")

    if instrumental:
        parts.append("instrumental")

    prompt_text = ", ".join(parts) if parts else "ambient background music"

    return SunoPrompt(
        prompt=prompt_text,
        style=style,
        instrumental=instrumental,
    )
