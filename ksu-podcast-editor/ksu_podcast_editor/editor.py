"""Audio editing operations."""

from pathlib import Path

import numpy as np
import soundfile as sf
from pydub import AudioSegment

from .models import EditDecision


class Editor:
    """Edits audio files based on edit decisions."""

    def __init__(self, crossfade_ms: int = 20):
        """Initialize the editor.

        Args:
            crossfade_ms: Duration of crossfade in milliseconds
        """
        self.crossfade_ms = crossfade_ms

    def edit(
        self, input_path: Path, output_path: Path, decisions: list[EditDecision]
    ) -> None:
        """Edit an audio file by removing specified segments.

        Args:
            input_path: Path to input WAV file
            output_path: Path to output WAV file
            decisions: List of edit decisions (segments to remove)
        """
        if not decisions:
            # No edits needed, just copy the file
            audio = AudioSegment.from_wav(str(input_path))
            audio.export(str(output_path), format="wav")
            return

        audio = AudioSegment.from_wav(str(input_path))

        # Sort decisions by start time in reverse order
        # This allows us to remove from the end first, preserving earlier timestamps
        sorted_decisions = sorted(decisions, key=lambda d: d.start, reverse=True)

        for decision in sorted_decisions:
            start_ms = int(decision.start * 1000)
            end_ms = int(decision.end * 1000)

            # Get the parts before and after the segment to remove
            before = audio[:start_ms]
            after = audio[end_ms:]

            # Apply crossfade if possible
            if len(before) >= self.crossfade_ms and len(after) >= self.crossfade_ms:
                audio = before.append(after, crossfade=self.crossfade_ms)
            else:
                audio = before + after

        audio.export(str(output_path), format="wav")

    def get_duration(self, audio_path: Path) -> float:
        """Get the duration of an audio file in seconds."""
        data, samplerate = sf.read(str(audio_path))
        return len(data) / samplerate
