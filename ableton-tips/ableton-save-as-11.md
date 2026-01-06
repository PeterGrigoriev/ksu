# How to Save Ableton Live 12 Projects for Ableton Live 11

## The Challenge
You have Ableton Live 12, but Ksu has Ableton Live 11. Live 11 cannot directly open Live 12 projects due to format differences.

## Solution: Export as Live 11 Project

### Step-by-Step Instructions

1. **Open your project in Ableton Live 12**
   - Load the project you want to share

2. **Save as Live 11 format**
   - Go to `File` → `Save Live Set as...`
   - In the save dialog, look for the dropdown menu at the bottom
   - Select **"Save as Live 11 Project"** from the format options
   - Choose a location and name for the exported project
   - Click Save

3. **What gets exported**
   - The entire project folder with all samples
   - Audio files and clips
   - MIDI data
   - Device settings (where compatible)
   - Arrangement and Session view data

### Important Considerations

#### Features that won't transfer
- **Live 12-exclusive devices**: Any Live 12-only devices will be disabled or replaced with placeholder devices
- **Live 12-specific features**: New automation modes, scale awareness features, or other Live 12-only functionality
- **Some Max for Live devices**: May not be compatible if they use Live 12-specific APIs

#### Before exporting
1. **Collect All and Save**: First do `File` → `Collect All and Save` to ensure all samples are in the project folder
2. **Freeze tracks with Live 12 devices**: If you used Live 12-exclusive devices, freeze those tracks first
3. **Check third-party plugins**: Ensure Ksu has the same third-party plugins you used

### Sharing the Project

After exporting:
1. **Zip the entire project folder** (not just the .als file)
2. Send the zipped folder to Ksu
3. She can unzip and open it normally in Live 11

### Working Together

#### Best practices for collaboration:
- **Stick to Live 11 features**: When working on shared projects, avoid using Live 12-exclusive features
- **Use "Collect All and Save"**: Always collect samples before sharing
- **Document plugin usage**: Keep a list of any third-party plugins used
- **Regular backups**: Both of you should keep versioned backups

#### Alternative: Stem Export
If the Live 11 export has too many compatibility issues:
1. Export individual tracks as audio stems (`File` → `Export Audio/Video`)
2. Share the stem files
3. Ksu can import them into a new Live 11 project

### Quick Reference
- **Menu path**: File → Save Live Set as... → Save as Live 11 Project
- **Always**: Collect All and Save first
- **Include**: The entire project folder when sharing
- **Freeze**: Tracks with Live 12-exclusive devices before export