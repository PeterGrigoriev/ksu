"""Download Suno tracks as MP3 files."""

import os
from pathlib import Path

import httpx


async def download_track(
    audio_url: str,
    output_dir: str | Path | None = None,
    filename: str | None = None,
) -> Path:
    """
    Download a track from URL to local file.

    Args:
        audio_url: URL to the audio file
        output_dir: Directory to save the file (defaults to ./output)
        filename: Custom filename (defaults to extracted from URL)

    Returns:
        Path to the downloaded file
    """
    # Determine output directory
    if output_dir is None:
        output_dir = os.environ.get("SUNO_OUTPUT_DIR", "./output")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Determine filename
    if filename is None:
        # Extract from URL or generate
        url_filename = audio_url.split("/")[-1].split("?")[0]
        if url_filename and url_filename.endswith(".mp3"):
            filename = url_filename
        else:
            import uuid
            filename = f"suno_{uuid.uuid4().hex[:8]}.mp3"

    # Ensure .mp3 extension
    if not filename.endswith(".mp3"):
        filename = f"{filename}.mp3"

    file_path = output_path / filename

    # Download the file
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.get(audio_url)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

    return file_path
