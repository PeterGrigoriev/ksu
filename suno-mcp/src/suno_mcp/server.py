"""MCP server for Suno music generation."""

import asyncio
import json
import os
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .downloader import download_track
from .prompt_generator import ConversationAnalysis, SunoPrompt, generate_prompt
from .suno_client import SunoClient

server = Server("suno-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="analyze_conversation",
            description=(
                "Analyze a client conversation to extract themes, emotions, and mood "
                "suitable for music generation. Returns structured analysis."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "conversation": {
                        "type": "string",
                        "description": "The raw conversation text to analyze",
                    },
                    "mood": {
                        "type": "string",
                        "description": "Detected mood (e.g., happy, melancholic, energetic)",
                    },
                    "themes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Key themes from the conversation",
                    },
                    "emotions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Emotions present in the conversation",
                    },
                    "suggested_genres": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Music genres that would fit the conversation",
                    },
                    "energy_level": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Overall energy level of the conversation",
                    },
                },
                "required": ["conversation", "mood", "themes", "emotions", "suggested_genres", "energy_level"],
            },
        ),
        Tool(
            name="generate_suno_prompt",
            description=(
                "Generate an optimized prompt for Suno API based on analysis results "
                "or direct input. Returns a prompt ready for track creation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "mood": {
                        "type": "string",
                        "description": "The mood for the music",
                    },
                    "themes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Themes to incorporate",
                    },
                    "style": {
                        "type": "string",
                        "description": "Music style/genre",
                    },
                    "instrumental": {
                        "type": "boolean",
                        "description": "Whether to create instrumental music (no vocals)",
                        "default": False,
                    },
                    "custom_prompt": {
                        "type": "string",
                        "description": "Optional custom prompt to use directly",
                    },
                },
            },
        ),
        Tool(
            name="create_track",
            description=(
                "Create a music track using the Suno API. "
                "Returns track ID for status checking and download."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The music generation prompt",
                    },
                    "title": {
                        "type": "string",
                        "description": "Optional title for the track",
                    },
                    "style": {
                        "type": "string",
                        "description": "Optional style/genre",
                    },
                    "instrumental": {
                        "type": "boolean",
                        "description": "Create instrumental track",
                        "default": False,
                    },
                },
                "required": ["prompt"],
            },
        ),
        Tool(
            name="get_track_status",
            description="Check the status of a track being generated.",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_id": {
                        "type": "string",
                        "description": "The track ID to check",
                    },
                },
                "required": ["track_id"],
            },
        ),
        Tool(
            name="download_track",
            description="Download a completed track as MP3 file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_id": {
                        "type": "string",
                        "description": "The track ID to download",
                    },
                    "filename": {
                        "type": "string",
                        "description": "Optional custom filename for the MP3",
                    },
                },
                "required": ["track_id"],
            },
        ),
        Tool(
            name="generate_and_download",
            description=(
                "End-to-end workflow: generate a track from prompt and download as MP3. "
                "Waits for completion and returns the local file path."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The music generation prompt",
                    },
                    "title": {
                        "type": "string",
                        "description": "Optional title for the track",
                    },
                    "style": {
                        "type": "string",
                        "description": "Optional style/genre",
                    },
                    "instrumental": {
                        "type": "boolean",
                        "description": "Create instrumental track",
                        "default": False,
                    },
                    "filename": {
                        "type": "string",
                        "description": "Optional custom filename for the MP3",
                    },
                },
                "required": ["prompt"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""

    if name == "analyze_conversation":
        # Store the analysis provided by Claude
        analysis = ConversationAnalysis(
            mood=arguments["mood"],
            themes=arguments["themes"],
            emotions=arguments["emotions"],
            suggested_genres=arguments["suggested_genres"],
            key_phrases=arguments.get("key_phrases", []),
            energy_level=arguments["energy_level"],
            summary=arguments.get("summary", ""),
        )
        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "success",
                "analysis": analysis.model_dump(),
            }, indent=2),
        )]

    elif name == "generate_suno_prompt":
        if custom_prompt := arguments.get("custom_prompt"):
            prompt = SunoPrompt(
                prompt=custom_prompt,
                style=arguments.get("style"),
                instrumental=arguments.get("instrumental", False),
            )
        else:
            prompt = generate_prompt(
                mood=arguments.get("mood"),
                themes=arguments.get("themes"),
                style=arguments.get("style"),
                instrumental=arguments.get("instrumental", False),
            )
        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "success",
                "prompt": prompt.model_dump(),
            }, indent=2),
        )]

    elif name == "create_track":
        client = SunoClient()
        try:
            track = await client.create_track(
                prompt=arguments["prompt"],
                title=arguments.get("title"),
                style=arguments.get("style"),
                instrumental=arguments.get("instrumental", False),
            )
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "track": track.model_dump(),
                }, indent=2),
            )]
        finally:
            await client.close()

    elif name == "get_track_status":
        client = SunoClient()
        try:
            track = await client.get_track(arguments["track_id"])
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "track": track.model_dump(),
                }, indent=2),
            )]
        finally:
            await client.close()

    elif name == "download_track":
        client = SunoClient()
        try:
            track = await client.get_track(arguments["track_id"])
            if not track.audio_url:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "message": f"Track {arguments['track_id']} is not ready for download. Status: {track.status}",
                    }, indent=2),
                )]

            file_path = await download_track(
                audio_url=track.audio_url,
                filename=arguments.get("filename"),
            )
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "file_path": str(file_path.absolute()),
                    "track": track.model_dump(),
                }, indent=2),
            )]
        finally:
            await client.close()

    elif name == "generate_and_download":
        client = SunoClient()
        try:
            # Create track
            track = await client.create_track(
                prompt=arguments["prompt"],
                title=arguments.get("title"),
                style=arguments.get("style"),
                instrumental=arguments.get("instrumental", False),
            )

            # Wait for completion
            track = await client.wait_for_track(track.id)

            # Download
            file_path = await download_track(
                audio_url=track.audio_url,
                filename=arguments.get("filename"),
            )

            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "file_path": str(file_path.absolute()),
                    "track": track.model_dump(),
                }, indent=2),
            )]
        except TimeoutError as e:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "error",
                    "message": str(e),
                }, indent=2),
            )]
        except RuntimeError as e:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "error",
                    "message": str(e),
                }, indent=2),
            )]
        finally:
            await client.close()

    else:
        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "error",
                "message": f"Unknown tool: {name}",
            }, indent=2),
        )]


def main():
    """Run the MCP server."""
    asyncio.run(stdio_server(server))


if __name__ == "__main__":
    main()
