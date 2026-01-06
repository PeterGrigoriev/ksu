# Suno MCP Server

An MCP (Model Context Protocol) server that generates music using the Suno API based on client conversation analysis.

## Purpose

This server enables Claude to:
1. Analyze client conversations and extract emotional themes, moods, and key concepts
2. Generate creative music prompts suitable for Suno AI
3. Call the Suno API to create music tracks
4. Download generated tracks as MP3 files

## Directory Structure

```
suno-mcp/
├── AGENT.md                 # This file - project documentation
├── pyproject.toml           # Python project configuration (uv)
├── src/
│   └── suno_mcp/
│       ├── __init__.py
│       ├── server.py        # MCP server implementation
│       ├── suno_client.py   # Suno API client
│       ├── prompt_generator.py  # Conversation-to-prompt logic
│       └── downloader.py    # MP3 download functionality
├── tests/
│   └── test_prompt_generator.py
└── output/                  # Downloaded MP3 files (gitignored)
```

## Tools Provided

### 1. `analyze_conversation`
Analyzes a client conversation and extracts themes, emotions, and key concepts suitable for music generation.

**Input:** Raw conversation text
**Output:** Structured analysis with mood, themes, suggested genres

### 2. `generate_suno_prompt`
Creates a Suno-compatible music prompt from conversation analysis or direct input.

**Input:** Conversation text or analysis results
**Output:** Optimized prompt for Suno API

### 3. `create_track`
Calls Suno API to generate a music track.

**Input:** Music prompt, optional parameters (style, duration, instrumental)
**Output:** Track ID and status

### 4. `download_track`
Downloads a generated track as MP3.

**Input:** Track ID
**Output:** Local file path to downloaded MP3

### 5. `generate_and_download`
End-to-end workflow: analyze conversation → generate prompt → create track → download MP3.

**Input:** Conversation text, optional style preferences
**Output:** Local file path(s) to downloaded MP3(s)

## Configuration

Set the following environment variables:
- `SUNO_API_KEY` - Your Suno Pro account API key
- `SUNO_OUTPUT_DIR` - (Optional) Custom output directory for MP3s

## Usage with Claude Desktop

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "suno": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/suno-mcp", "suno-mcp"],
      "env": {
        "SUNO_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run server directly
uv run suno-mcp
```
