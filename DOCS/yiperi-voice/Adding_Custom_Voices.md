# Adding Custom Voices

This guide walks you through the process of authoring and importing your own custom voice banks for **Yiperi Voice**.

The engine generates gibberish speech by playing combinations of up to **68 distinct phonetic tokens** (syllables, single consonants, and vowels). 

> [!TIP]
> Having 68 tokens is the **maximum set**, not a strict requirement. The engine features an automatic CV (consonant-vowel) fallback system. If a specific syllable clip is missing, it will automatically fallback to other available syllables in the same consonant group or to a plain vowel. At a minimum, providing just the 5 vowels and a small set of syllables (e.g., 5 consonant-vowel pairs) is enough to produce a functional voice. A prime example of this is the built-in `np` voice, which only includes `pa, pe, pi, po, pu` and `na, ne, ni, no, nu`.

Creating a custom voice involves providing voice clips in two variants: **Normal** and **Stressed**.

---

## The Complete Token Set (68 Tokens Max)

If you wish to create a complete voice bank, you can provide `.wav` files named after the following lowercase tokens:

*   **Vowels (5):** `a`, `e`, `i`, `o`, `u`
*   **Single Consonants (3):** `s`, `n`, `r`
*   **Consonant-Vowel (CV) pairs (60):**
    *   `pa`, `pe`, `pi`, `po`, `pu`
    *   `ta`, `te`, `ti`, `to`, `tu`
    *   `ka`, `ke`, `ki`, `ko`, `ku`
    *   `fa`, `fe`, `fi`, `fo`, `fu`
    *   `sa`, `se`, `si`, `so`, `su`
    *   `ma`, `me`, `mi`, `mo`, `mu`
    *   `na`, `ne`, `ni`, `no`, `nu`
    *   `la`, `le`, `li`, `lo`, `lu`
    *   `ra`, `re`, `ri`, `ro`, `ru`
    *   `wa`, `we`, `wi`, `wo`, `wu`
    *   `ya`, `ye`, `yi`, `yo`, `yu`
    *   `xa`, `xe`, `xi`, `xo`, `xu`

---

## Authoring Process

We provide several Python helper scripts in the `_DEV/audio-edit~` folder to assist with bulk processing, sizing, and click-prevention. 

> [!IMPORTANT]
> These Python scripts require dependencies such as `numpy` and `soundfile`. Make sure to install them before running (see `InstallAudioEditDeps.bat`).

### Step 1: Record and Name the Clips
1. Record yourself or generate synthesized sounds speaking the 68 tokens.
2. Cut each token out and save it as a `.wav` file named exactly like its token (e.g., `pa.wav`, `sa.wav`, `a.wav`).

### Step 2: Auto-Normalize Sizing (PrepareTokenClips.py)
In Yiperi Voice:
- **Normal** clips should ideally be around **100 ms** in length.
- **Stressed** clips should ideally be around **200 ms** in length, and pitched slightly higher (about **2 to 3 semitones**).

*Note: These durations are guidelines for best results, but the engine is highly flexible. The system will not break if clips are slightly shorter or longer.*

You can use the `PrepareTokenClips.py` script to automate pitch shifting, time stretching, padding, and edge fading. Edit the configuration variables at the top of `PrepareTokenClips.py` for each pass:

*   **For Normal clips:**
    ```python
    INPUT_FOLDER = "your_raw_normal_recordings"
    OUTPUT_FOLDER = "voice_custom_normal"
    TARGET_MS = 100
    PITCH_SEMITONES = 0
    ```
*   **For Stressed clips:**
    ```python
    INPUT_FOLDER = "your_raw_stressed_recordings"
    OUTPUT_FOLDER = "voice_custom_stress"
    TARGET_MS = 200
    PITCH_SEMITONES = 2 # Or 3 semitones higher
    ```

Run the script to output uniform, perfectly-sized audio clips.

---

## Bulk Processing Workflow (Optional)

If you want to apply complex audio effects (like robotic ring modulation, filters, radio distortion, or EQ) to all 68 clips at once, you can use the Join/Split pipeline:

### 1. Join Clips into a Single Track
Set `SOURCE_FOLDER` in `JoinWavs.py` to your directory of processed clips. Running the script outputs a single file (`_joined.wav`) where each clip starts exactly every **1000 ms** (1 second).

### 2. Apply Effects in Your DAW
Import the joined `.wav` file into an external audio editor (e.g., Audacity, Adobe Audition, or Reaper). Apply your desired filters or effects to the entire track. Export the resulting audio back to a `.wav` file.

### 3. Split the Edited Track
Set `INPUT_WAV` (the edited file) and `OUTPUT_FOLDER` in `SplitJoined.py`. Set `CLIP_MS` to match the duration of the clips (e.g., `100` for normal or `200` for stressed). Run the script to automatically slice the joined track back into 68 individual `.wav` files named after their respective tokens.

### 4. Remove Audio Clicks (TestFadeNeed.py)
After splitting or applying heavy audio effects, some clips might suffer from micro-clicks at their start or end. Run `TestFadeNeed.py` to analyze the edge envelopes of the WAV files and automatically apply a soft fade-in/fade-out only where needed.

---

## Importing Into Unity

To integrate your new voice into the game:

1. Create a folder inside `Assets/.../Resources/Yiperi-voice/Sounds/` named `voice_[your_voice_name]`.
2. Move your **Normal** `.wav` files directly into that folder.
3. Create a subfolder inside it called `stress` (i.e. `voice_[your_voice_name]/stress`).
4. Move your **Stressed** `.wav` files into the `stress` folder.
5. In your code, load and play the voice using its identifier:
    ```csharp
    VoicePlayer.LoadVoice("your_voice_name");
    ```
