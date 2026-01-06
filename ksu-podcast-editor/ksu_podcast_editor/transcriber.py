"""Speech-to-text transcription with timestamps."""

import logging
from pathlib import Path

from faster_whisper import WhisperModel

from .models import Segment, Word

logger = logging.getLogger(__name__)


class Transcriber:
    """Transcribes audio files using faster-whisper."""

    def __init__(self, model_size: str = "large-v3", device: str = "auto", verbose: bool = False):
        """Initialize the transcriber.

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large-v3)
            device: Device to use (auto, cpu, cuda)
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        logger.info(f"Loading Whisper model: {model_size} (device={device})")
        if verbose:
            print(f"[DEBUG] Loading Whisper model: {model_size} (device={device})")
            print("[DEBUG] This may take a while on first run (downloading model)...")
        self.model = WhisperModel(model_size, device=device, compute_type="auto")
        logger.info("Model loaded successfully")
        if verbose:
            print("[DEBUG] Model loaded successfully")

    def transcribe(self, audio_path: Path, language: str | None = None) -> list[Segment]:
        """Transcribe an audio file.

        Args:
            audio_path: Path to the audio file
            language: Language code (e.g., "ru", "en") or None for auto-detect

        Returns:
            List of segments with word-level timestamps
        """
        logger.info(f"Starting transcription: {audio_path}")
        if self.verbose:
            print(f"[DEBUG] Starting transcription of: {audio_path}")
            print(f"[DEBUG] Language: {language or 'auto-detect'}")

        segments, info = self.model.transcribe(
            str(audio_path),
            language=language,
            word_timestamps=True,
        )

        if self.verbose:
            print(f"[DEBUG] Detected language: {info.language} (probability: {info.language_probability:.2f})")
            print("[DEBUG] Processing segments...")

        result = []
        segment_count = 0
        for segment in segments:
            segment_count += 1
            if self.verbose and segment_count % 10 == 0:
                print(f"[DEBUG] Processed {segment_count} segments, current: {segment.start:.1f}s - {segment.end:.1f}s")
            words = []
            if segment.words:
                for word in segment.words:
                    words.append(
                        Word(
                            text=word.word.strip(),
                            start=word.start,
                            end=word.end,
                            confidence=word.probability,
                        )
                    )

            result.append(
                Segment(
                    start=segment.start,
                    end=segment.end,
                    words=words,
                    text=segment.text.strip(),
                )
            )

        logger.info(f"Transcription complete: {len(result)} segments")
        if self.verbose:
            print(f"[DEBUG] Transcription complete: {segment_count} segments processed")
            total_words = sum(len(s.words) for s in result)
            print(f"[DEBUG] Total words extracted: {total_words}")

        return result
