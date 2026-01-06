"""Filler and repetition detection."""

from .models import EditDecision, Segment, Word

# Single-word fillers by language
FILLERS = {
    "ru": {
        # Hesitation sounds
        "э", "ээ", "эээ", "м", "мм", "ммм", "а", "аа", "ааа",
        # Common filler words
        "ну", "вот", "типа", "значит", "короче", "вообще", "там",
        "так", "это", "ладно", "блин", "слушай", "смотри",
        "понимаешь", "знаешь", "видишь", "представляешь",
        "допустим", "наверное", "кстати", "прикинь",
    },
    "en": {
        "um", "uh", "hmm", "like", "you know", "so", "basically",
        "erm", "ah", "well", "right", "okay", "anyway",
    },
}

# Multi-word filler phrases (checked separately)
FILLER_PHRASES = {
    "ru": [
        "как бы", "ну вот", "вот так", "это самое", "так сказать",
        "в общем", "в принципе", "в смысле", "по сути",
        "на самом деле", "собственно говоря", "честно говоря",
        "грубо говоря", "короче говоря", "скажем так",
        "как говорится", "так называемый", "можно сказать",
        "ну типа", "ну короче", "ну это", "вот это",
    ],
    "en": [
        "you know", "i mean", "kind of", "sort of", "you see",
        "to be honest", "basically speaking", "at the end of the day",
    ],
}


class Analyzer:
    """Analyzes transcribed segments for fillers and repetitions."""

    def __init__(self, language: str = "ru", custom_fillers: set[str] | None = None):
        """Initialize the analyzer.

        Args:
            language: Language code ("ru" or "en")
            custom_fillers: Additional filler words to detect
        """
        self.language = language
        self.fillers = FILLERS.get(language, set())
        self.filler_phrases = FILLER_PHRASES.get(language, [])
        if custom_fillers:
            self.fillers = self.fillers | custom_fillers

    def analyze(self, segments: list[Segment]) -> list[EditDecision]:
        """Analyze segments and return edit decisions.

        Args:
            segments: List of transcribed segments

        Returns:
            List of edit decisions for segments to remove
        """
        decisions = []

        all_words = []
        for segment in segments:
            all_words.extend(segment.words)

        # Track which word indices are already marked (to avoid double-counting)
        marked_indices: set[int] = set()

        # Detect multi-word filler phrases first
        for phrase in self.filler_phrases:
            phrase_words = phrase.split()
            phrase_len = len(phrase_words)

            for i in range(len(all_words) - phrase_len + 1):
                if any(idx in marked_indices for idx in range(i, i + phrase_len)):
                    continue

                candidate = [self._normalize(all_words[j].text) for j in range(i, i + phrase_len)]
                if candidate == phrase_words:
                    # Found a phrase match
                    start_time = all_words[i].start
                    end_time = all_words[i + phrase_len - 1].end
                    original = " ".join(all_words[j].text for j in range(i, i + phrase_len))

                    decisions.append(
                        EditDecision(
                            start=start_time,
                            end=end_time,
                            reason="filler",
                            original_text=original,
                        )
                    )
                    for idx in range(i, i + phrase_len):
                        marked_indices.add(idx)

        # Detect single-word fillers
        for i, word in enumerate(all_words):
            if i in marked_indices:
                continue
            if self._is_filler(word):
                decisions.append(
                    EditDecision(
                        start=word.start,
                        end=word.end,
                        reason="filler",
                        original_text=word.text,
                    )
                )
                marked_indices.add(i)

        # Detect repetitions
        for i in range(1, len(all_words)):
            if i in marked_indices:
                continue
            if self._is_repetition(all_words[i - 1], all_words[i]):
                decisions.append(
                    EditDecision(
                        start=all_words[i].start,
                        end=all_words[i].end,
                        reason="repetition",
                        original_text=all_words[i].text,
                    )
                )

        # Sort by start time
        decisions.sort(key=lambda d: d.start)

        return decisions

    def _normalize(self, text: str) -> str:
        """Normalize text for comparison."""
        return text.lower().strip().rstrip(".,!?:;")

    def _is_filler(self, word: Word) -> bool:
        """Check if a word is a filler."""
        text = self._normalize(word.text)
        return text in self.fillers

    def _is_repetition(self, prev_word: Word, curr_word: Word) -> bool:
        """Check if current word is a repetition of the previous word."""
        prev_text = self._normalize(prev_word.text)
        curr_text = self._normalize(curr_word.text)
        return prev_text == curr_text and len(prev_text) > 1
