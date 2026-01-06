"""Command-line interface."""

import csv
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .analyzer import Analyzer
from .editor import Editor
from .transcriber import Transcriber

app = typer.Typer(help="KSU Podcast Editor - Remove fillers and repetitions from audio")
console = Console()


def _save_results(segments: list, decisions: list, output_path: Path, verbose: bool = False) -> None:
    """Save transcription and analysis results to file."""
    # Build data structure with all words and their labels
    all_words = []
    decision_map = {}  # Map (start, end) -> decision for quick lookup

    for decision in decisions:
        decision_map[(round(decision.start, 3), round(decision.end, 3))] = decision

    for segment in segments:
        for word in segment.words:
            word_key = (round(word.start, 3), round(word.end, 3))
            decision = decision_map.get(word_key)

            word_data = {
                "text": word.text,
                "start": round(word.start, 3),
                "end": round(word.end, 3),
                "confidence": round(word.confidence, 3),
                "label": decision.reason if decision else "keep",
            }
            all_words.append(word_data)

    ext = output_path.suffix.lower()

    if ext == ".json":
        output_data = {
            "segments": [
                {
                    "text": s.text,
                    "start": round(s.start, 3),
                    "end": round(s.end, 3),
                    "words": [
                        {
                            "text": w.text,
                            "start": round(w.start, 3),
                            "end": round(w.end, 3),
                            "confidence": round(w.confidence, 3),
                        }
                        for w in s.words
                    ],
                }
                for s in segments
            ],
            "words": all_words,
            "fillers": [
                {
                    "text": d.original_text,
                    "start": round(d.start, 3),
                    "end": round(d.end, 3),
                    "reason": d.reason,
                }
                for d in decisions
            ],
            "summary": {
                "total_segments": len(segments),
                "total_words": len(all_words),
                "fillers_count": len(decisions),
            },
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

    elif ext == ".csv":
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["text", "start", "end", "confidence", "label"])
            writer.writeheader()
            writer.writerows(all_words)

    else:
        # Default to plain text
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Transcription Results\n\n")
            f.write("## Words with timestamps\n\n")
            for word in all_words:
                label_str = f" [{word['label']}]" if word['label'] != "keep" else ""
                f.write(f"{word['start']:.3f} - {word['end']:.3f}: {word['text']}{label_str}\n")
            f.write(f"\n## Summary\n")
            f.write(f"Total words: {len(all_words)}\n")
            f.write(f"Fillers to remove: {len(decisions)}\n")

    if verbose:
        print(f"[DEBUG] Saved {len(all_words)} words to {output_path}")


@app.command()
def analyze(
    input_file: Path = typer.Argument(..., help="Input audio file (WAV or MP3)"),
    language: Optional[str] = typer.Option(
        None, "--language", "-l", help="Language code (ru/en), auto-detect if not specified"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose debug output"
    ),
    model: str = typer.Option(
        "large-v3", "--model", "-m", help="Whisper model size (tiny, base, small, medium, large-v3)"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Save results to file (JSON or CSV based on extension)"
    ),
) -> None:
    """Analyze audio file and show detected fillers without editing."""
    if not input_file.exists():
        console.print(f"[red]Error: File not found: {input_file}[/red]")
        raise typer.Exit(1)

    if verbose:
        console.print(f"[dim][DEBUG] Input file: {input_file}[/dim]")
        console.print(f"[dim][DEBUG] File size: {input_file.stat().st_size / 1024 / 1024:.1f} MB[/dim]")
        console.print(f"[dim][DEBUG] Model: {model}[/dim]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        disable=verbose,  # Disable spinner in verbose mode for cleaner output
    ) as progress:
        progress.add_task("Transcribing audio...", total=None)
        transcriber = Transcriber(model_size=model, verbose=verbose)
        segments = transcriber.transcribe(input_file, language=language)

    detected_lang = language or "auto"
    analyzer = Analyzer(language=language or "ru")
    decisions = analyzer.analyze(segments)

    # Save to file if requested
    if output:
        _save_results(segments, decisions, output, verbose)
        console.print(f"[green]Results saved to: {output}[/green]")

    # Display results
    table = Table(title="Detected Fillers and Repetitions")
    table.add_column("Time", style="cyan")
    table.add_column("Text", style="yellow")
    table.add_column("Reason", style="magenta")

    for decision in decisions:
        time_str = f"{decision.start:.2f}s - {decision.end:.2f}s"
        table.add_row(time_str, decision.original_text, decision.reason)

    console.print(table)
    console.print(f"\n[green]Found {len(decisions)} items to remove[/green]")


@app.command()
def edit(
    input_file: Path = typer.Argument(..., help="Input audio file (WAV or MP3)"),
    output_file: Path = typer.Argument(..., help="Output WAV file"),
    language: Optional[str] = typer.Option(
        None, "--language", "-l", help="Language code (ru/en), auto-detect if not specified"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-n", help="Show what would be removed without editing"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose debug output"
    ),
    model: str = typer.Option(
        "large-v3", "--model", "-m", help="Whisper model size (tiny, base, small, medium, large-v3)"
    ),
) -> None:
    """Process audio file and remove fillers and repetitions."""
    if not input_file.exists():
        console.print(f"[red]Error: File not found: {input_file}[/red]")
        raise typer.Exit(1)

    if verbose:
        console.print(f"[dim][DEBUG] Input file: {input_file}[/dim]")
        console.print(f"[dim][DEBUG] File size: {input_file.stat().st_size / 1024 / 1024:.1f} MB[/dim]")
        console.print(f"[dim][DEBUG] Model: {model}[/dim]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        disable=verbose,
    ) as progress:
        task = progress.add_task("Transcribing audio...", total=None)
        transcriber = Transcriber(model_size=model, verbose=verbose)
        segments = transcriber.transcribe(input_file, language=language)

        progress.update(task, description="Analyzing content...")
        analyzer = Analyzer(language=language or "ru")
        decisions = analyzer.analyze(segments)

        if dry_run:
            progress.stop()
            console.print(f"[yellow]Dry run - would remove {len(decisions)} segments[/yellow]")
            for decision in decisions:
                console.print(
                    f"  {decision.start:.2f}s - {decision.end:.2f}s: "
                    f"[{decision.reason}] {decision.original_text}"
                )
            return

        progress.update(task, description="Editing audio...")
        editor = Editor()
        editor.edit(input_file, output_file, decisions)

    # Show summary
    editor = Editor()
    original_duration = editor.get_duration(input_file)
    new_duration = editor.get_duration(output_file)
    saved_time = original_duration - new_duration

    console.print(f"\n[green]Done![/green]")
    console.print(f"Original duration: {original_duration:.2f}s")
    console.print(f"New duration: {new_duration:.2f}s")
    console.print(f"Saved: {saved_time:.2f}s ({saved_time/original_duration*100:.1f}%)")
    console.print(f"Output saved to: {output_file}")


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
