#!/usr/bin/env python3
"""Edit audio files using ffmpeg based on a JSON cuts file."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def load_cuts(json_path: Path) -> list[dict]:
    """Load cuts from JSON file and sort by start time descending."""
    with open(json_path) as f:
        data = json.load(f)

    cuts = data.get("cuts", data)  # Support both {"cuts": [...]} and [...]
    if isinstance(cuts, dict):
        cuts = list(cuts.values())

    # Sort by start time descending (last first to preserve timestamps)
    return sorted(cuts, key=lambda x: x["start"], reverse=True)


def get_duration(audio_path: Path) -> float:
    """Get audio duration in seconds using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio_path)
        ],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def remove_segment(input_path: Path, output_path: Path, start: float, end: float) -> None:
    """Remove a segment from audio using ffmpeg filter_complex."""
    # Use filter_complex to select parts before and after the cut, then concatenate
    filter_cmd = (
        f"[0]atrim=0:{start},asetpts=PTS-STARTPTS[a];"
        f"[0]atrim={end},asetpts=PTS-STARTPTS[b];"
        f"[a][b]concat=n=2:v=0:a=1[out]"
    )

    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(input_path),
            "-filter_complex", filter_cmd,
            "-map", "[out]",
            str(output_path)
        ],
        capture_output=True, check=True
    )


def edit_audio(input_path: Path, output_path: Path, cuts: list[dict], verbose: bool = False) -> None:
    """Apply all cuts to audio file, processing from last to first."""
    if not cuts:
        print("No cuts to apply")
        subprocess.run(["cp", str(input_path), str(output_path)])
        return

    # Work with temp files for intermediate steps
    current_input = input_path

    for i, cut in enumerate(cuts):
        start, end = cut["start"], cut["end"]

        if verbose:
            text_preview = cut.get("text", "")[:50]
            print(f"  [{i+1}/{len(cuts)}] Removing {start:.1f}s - {end:.1f}s: {text_preview}...")

        # Use temp file for intermediate, final file for last cut
        is_last = (i == len(cuts) - 1)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        target = output_path if is_last else tmp_path

        try:
            remove_segment(current_input, target, start, end)
        except subprocess.CalledProcessError as e:
            print(f"Error processing cut at {start:.1f}s: {e}")
            raise

        # Clean up previous temp file (but not original input)
        if current_input != input_path:
            current_input.unlink()

        current_input = target


def main():
    parser = argparse.ArgumentParser(description="Edit audio using ffmpeg based on JSON cuts file")
    parser.add_argument("input", type=Path, help="Input audio file")
    parser.add_argument("output", type=Path, help="Output audio file")
    parser.add_argument("cuts_json", type=Path, help="JSON file with cuts to remove")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show progress")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1

    if not args.cuts_json.exists():
        print(f"Error: Cuts file not found: {args.cuts_json}")
        return 1

    cuts = load_cuts(args.cuts_json)
    print(f"Loaded {len(cuts)} cuts from {args.cuts_json}")

    original_duration = get_duration(args.input)
    print(f"Original duration: {original_duration:.1f}s ({original_duration/60:.1f} min)")

    print(f"Applying cuts...")
    edit_audio(args.input, args.output, cuts, verbose=args.verbose)

    new_duration = get_duration(args.output)
    saved = original_duration - new_duration

    print(f"\nDone!")
    print(f"New duration: {new_duration:.1f}s ({new_duration/60:.1f} min)")
    print(f"Removed: {saved:.1f}s ({saved/60:.1f} min)")
    print(f"Output: {args.output}")

    return 0


if __name__ == "__main__":
    exit(main())
