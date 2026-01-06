# Local Podcast Editing Automation (Reaper + Auto-Cut)

## Goal

Build a **fully local** system that:
- Takes a WAV file
- Produces **word-level timestamps** (English + Russian)
- Detects **fillers** and **repetitions**
- Automatically **cuts those regions in Reaper** using regions + ripple delete

Target platform:
- macOS (Apple Silicon M1)
- Reaper as the DAW
- Offline, deterministic, scriptable

---

## High-Level Architecture

WAV
 ↓
Audio normalization (ffmpeg)
 ↓
Speech-to-text + word alignment
 ↓
words.json  (rich, internal)
 ↓
Issue detection (Python)
 ↓
cuts.csv    (flat, execution format)
 ↓
ReaScript (Lua)
 ↓
Regions → auto-cut in Reaper

Design principle:
- Python does analysis
- Lua executes edits
- CSV is the boundary format

---

## Execution Output (Reaper Boundary)

File: cuts.csv

Format:
start_sec,end_sec,label

Example:
12.430,12.860,FILLER: um
45.120,45.610,REPEAT: i i
103.500,104.020,FILLER: эм
