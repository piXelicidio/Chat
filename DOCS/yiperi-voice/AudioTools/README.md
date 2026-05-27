# Audio Tools

This directory contains Python scripts to help prepare, process, and package audio clips for custom voice banks in **Yiperi Voice**.

## Included Scripts

### 1. `PrepareTokenClips.py`
Automates pitch shifting, time stretching, padding, and edge fading to normalize the duration of your audio clips.
- **Normal clips** should be exactly **100 ms** at 0 pitch shift.
- **Stressed clips** should be exactly **200 ms** and pitched slightly higher (about 2 to 3 semitones).

### 2. `JoinWavs.py`
Joins all 68 individual token clips in a folder into a single unified WAV track (`_joined.wav`) with 1-second (1000 ms) intervals. This allows you to easily import the joined track into a DAW (like Audacity or Reaper) to apply bulk audio effects (EQ, distortion, etc.) all at once.

### 3. `SplitJoined.py`
Takes a joined WAV track (which has been edited or processed in your DAW) and automatically slices it back into 68 individual WAV files named after their respective tokens.

---

## Detailed Guide
For step-by-step instructions on recording, preparing, and importing custom voice banks into Unity, see the main [Adding Custom Voices](../Adding_Custom_Voices.md) guide.
