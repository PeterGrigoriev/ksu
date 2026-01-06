# Shared Folder Structure for Music Collaboration

## Setup on Mac Mini

Run this command to create the folder structure:

```bash
mkdir -p ~/Shared/{Projects/{Ableton,Logic,Exports},Assets/{Samples,Stems,References},Archive}
```

## Folder Structure

```
Shared/
├── Projects/
│   ├── Ableton/          # Ableton Live projects (.als + folders)
│   ├── Logic/            # Logic Pro projects (.logicx bundles)
│   └── Exports/          # Bounced mixes, masters, stems for review
│
├── Assets/
│   ├── Samples/          # Shared sample libraries, loops, one-shots
│   ├── Stems/            # Individual track exports for mixing
│   └── References/       # Reference tracks, inspiration
│
└── Archive/              # Completed projects, old versions
```

## Usage Guidelines

### Projects/Ableton/
- Create subfolders per song: `SongName_v1/`
- Include "Collect All and Save" to bundle samples
- Use version numbers: `SongName_v1.als`, `SongName_v2.als`

### Projects/Logic/
- Logic bundles everything in `.logicx` automatically
- Still use version naming: `SongName_v1.logicx`

### Projects/Exports/
- Naming: `SongName_YYYYMMDD_mix1.wav`
- Keep notes: `SongName_notes.txt` for feedback

### Assets/Samples/
- Organize by type: `Drums/`, `Synths/`, `Vocals/`, etc.
- Both users can add to shared library

### Archive/
- Move finished projects here
- Add date: `2024-12_AlbumName/`

## File Sharing Settings

On Mac Mini, share the entire `Shared/` folder:
1. System Settings → General → Sharing → File Sharing
2. Add `~/Shared` to Shared Folders
3. Set permissions: Both users = Read & Write

## Workflow Tips

- **Before opening a project**: Check if the other person has it open (avoid conflicts)
- **Ableton**: "Collect All and Save" before sharing new projects
- **Logic**: Projects are self-contained bundles, just copy
- **Large WAVs**: Put in `Stems/` or `Exports/`, reference from projects
