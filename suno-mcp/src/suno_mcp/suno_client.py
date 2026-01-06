"""Suno API client."""

import os
from enum import Enum

import httpx
from pydantic import BaseModel


class TrackStatus(str, Enum):
    """Status of a Suno track."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Track(BaseModel):
    """A Suno track."""

    id: str
    status: TrackStatus
    title: str | None = None
    audio_url: str | None = None
    duration: float | None = None
    prompt: str | None = None


class SunoClient:
    """Client for interacting with Suno API."""

    BASE_URL = "https://api.suno.ai/v1"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("SUNO_API_KEY")
        if not self.api_key:
            raise ValueError("SUNO_API_KEY is required")

        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )

    async def create_track(
        self,
        prompt: str,
        title: str | None = None,
        style: str | None = None,
        instrumental: bool = False,
    ) -> Track:
        """
        Create a new track using Suno API.

        Args:
            prompt: The music generation prompt
            title: Optional title for the track
            style: Optional style/genre
            instrumental: Whether to create an instrumental track

        Returns:
            Track object with ID and initial status
        """
        payload = {
            "prompt": prompt,
            "make_instrumental": instrumental,
        }

        if title:
            payload["title"] = title

        if style:
            payload["style"] = style

        response = await self.client.post("/generate", json=payload)
        response.raise_for_status()

        data = response.json()

        # Suno typically returns a list of tracks (usually 2)
        track_data = data["tracks"][0] if "tracks" in data else data

        return Track(
            id=track_data["id"],
            status=TrackStatus(track_data.get("status", "pending")),
            title=track_data.get("title"),
            prompt=prompt,
        )

    async def get_track(self, track_id: str) -> Track:
        """
        Get track status and details.

        Args:
            track_id: The track ID to look up

        Returns:
            Track object with current status
        """
        response = await self.client.get(f"/tracks/{track_id}")
        response.raise_for_status()

        data = response.json()

        return Track(
            id=data["id"],
            status=TrackStatus(data["status"]),
            title=data.get("title"),
            audio_url=data.get("audio_url"),
            duration=data.get("duration"),
            prompt=data.get("prompt"),
        )

    async def wait_for_track(
        self, track_id: str, poll_interval: float = 5.0, max_wait: float = 300.0
    ) -> Track:
        """
        Wait for a track to complete processing.

        Args:
            track_id: The track ID to wait for
            poll_interval: Seconds between status checks
            max_wait: Maximum seconds to wait

        Returns:
            Completed Track object

        Raises:
            TimeoutError: If track doesn't complete in time
            RuntimeError: If track generation fails
        """
        import asyncio

        elapsed = 0.0

        while elapsed < max_wait:
            track = await self.get_track(track_id)

            if track.status == TrackStatus.COMPLETED:
                return track

            if track.status == TrackStatus.FAILED:
                raise RuntimeError(f"Track generation failed: {track_id}")

            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        raise TimeoutError(f"Track {track_id} did not complete within {max_wait}s")

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
