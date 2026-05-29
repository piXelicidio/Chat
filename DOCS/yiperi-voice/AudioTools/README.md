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

## Dependencies & Installation

To run these scripts, you need **Python 3** installed on your system along with the following library dependencies and external tools:

### 1. Python Libraries
The scripts require `numpy`, `soundfile`, and `librosa`. Install them using `pip`:
```bash
pip install numpy soundfile librosa
```

### 2. External Tools
*   **Rubber Band CLI (`rubberband-r3`)**: Required by `PrepareTokenClips.py` for pitch-shifting and time-stretching.
    *   Download and install the **Rubber Band Library** command-line utility.
    *   Ensure the executable (typically `rubberband-r3` or `rubberband`) is added to your system's `PATH`.
    *   If your executable is named differently (e.g., just `rubberband`), update the `RUBBERBAND_EXE` variable at the top of `PrepareTokenClips.py`.

---

## Detailed Guide
For step-by-step instructions on recording, preparing, and importing custom voice banks into Unity, see the main [Adding Custom Voices](../Adding_Custom_Voices.md) guide.
