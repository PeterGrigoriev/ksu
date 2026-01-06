"""Tests for prompt generator."""

import pytest

from suno_mcp.prompt_generator import (
    ConversationAnalysis,
    SunoPrompt,
    generate_prompt,
)


def test_generate_prompt_with_mood():
    """Test prompt generation with just mood."""
    prompt = generate_prompt(mood="melancholic")
    assert "melancholic" in prompt.prompt.lower()


def test_generate_prompt_with_themes():
    """Test prompt generation with themes."""
    prompt = generate_prompt(themes=["love", "loss", "hope"])
    assert "love" in prompt.prompt.lower()


def test_generate_prompt_with_style():
    """Test prompt generation with style."""
    prompt = generate_prompt(style="jazz")
    assert "jazz" in prompt.prompt.lower()
    assert prompt.style == "jazz"


def test_generate_prompt_instrumental():
    """Test instrumental flag."""
    prompt = generate_prompt(mood="calm", instrumental=True)
    assert prompt.instrumental is True
    assert "instrumental" in prompt.prompt.lower()


def test_generate_prompt_from_analysis():
    """Test prompt generation from full analysis."""
    analysis = ConversationAnalysis(
        mood="hopeful",
        themes=["new beginnings", "growth"],
        emotions=["optimism", "excitement"],
        suggested_genres=["indie", "folk"],
        key_phrases=["fresh start"],
        energy_level="medium",
        summary="A conversation about starting over.",
    )

    prompt = generate_prompt(analysis=analysis)

    assert "hopeful" in prompt.prompt.lower()
    assert prompt.style == "indie"


def test_generate_prompt_empty():
    """Test prompt generation with no input."""
    prompt = generate_prompt()
    assert prompt.prompt  # Should have default


def test_conversation_analysis_model():
    """Test ConversationAnalysis model."""
    analysis = ConversationAnalysis(
        mood="happy",
        themes=["celebration"],
        emotions=["joy"],
        suggested_genres=["pop"],
        key_phrases=["congratulations"],
        energy_level="high",
        summary="A celebration.",
    )

    assert analysis.mood == "happy"
    assert analysis.energy_level == "high"


def test_suno_prompt_model():
    """Test SunoPrompt model."""
    prompt = SunoPrompt(
        prompt="happy celebration music",
        style="pop",
        title="Celebration",
        instrumental=False,
    )

    assert prompt.prompt == "happy celebration music"
    assert prompt.title == "Celebration"
