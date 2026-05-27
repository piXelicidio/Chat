"""
Joined-WAV splitter.
Reads `INPUT_WAV`, uses the sorted token list to cut one clip every
`START_INTERVAL_MS`, takes `CLIP_MS` from each start position, and saves the
clips into `OUTPUT_FOLDER` as token-named WAV files.
"""

from pathlib import Path

import numpy as np
import soundfile as sf


INPUT_WAV = "wiwi_stress_joined.wav"
OUTPUT_FOLDER = "voice_retro\\stress"
CLIP_MS = 205
START_INTERVAL_MS = 1000

TOKENS = [
    "a", "e", "i", "o", "u",
    "s", "n", "r",
    "pa", "pe", "pi", "po", "pu",
    "ta", "te", "ti", "to", "tu",
    "ka", "ke", "ki", "ko", "ku",
    "fa", "fe", "fi", "fo", "fu",
    "sa", "se", "si", "so", "su",
    "ma", "me", "mi", "mo", "mu",
    "na", "ne", "ni", "no", "nu",
    "la", "le", "li", "lo", "lu",
    "ra", "re", "ri", "ro", "ru",
    "wa", "we", "wi", "wo", "wu",
    "ya", "ye", "yi", "yo", "yu",
    "xa", "xe", "xi", "xo", "xu",
]


def get_clip_samples(sample_rate):
    return int(round(sample_rate * CLIP_MS / 1000.0))


def get_start_samples(sample_rate):
    return int(round(sample_rate * START_INTERVAL_MS / 1000.0))


def to_2d(audio):
    if audio.ndim == 1:
        return audio[:, np.newaxis]

    return audio


def fit_to_length(audio, target_samples):
    current_samples = len(audio)

    if current_samples == target_samples:
        return audio

    if current_samples > target_samples:
        return audio[:target_samples]

    padded = np.zeros((target_samples, audio.shape[1]), dtype=np.float32)
    padded[:current_samples, :] = audio
    return padded


def main():
    base_folder = Path(__file__).resolve().parent
    input_path = base_folder / INPUT_WAV
    output_folder = base_folder / OUTPUT_FOLDER

    if not input_path.exists():
        print(f"Input wav not found: {input_path}")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    audio, sample_rate = sf.read(input_path, always_2d=False)
    audio = np.asarray(audio, dtype=np.float32)
    audio = to_2d(audio)

    clip_samples = get_clip_samples(sample_rate)
    start_samples = get_start_samples(sample_rate)
    sorted_tokens = sorted(TOKENS)

    saved_count = 0

    for index, token in enumerate(sorted_tokens):
        start = index * start_samples
        end = start + clip_samples

        if start >= len(audio):
            print(f"Stopped at token {token}: start is outside the input wav")
            break

        clip = audio[start:end, :]
        clip = fit_to_length(clip, clip_samples)

        output_path = output_folder / f"{token}.wav"

        if clip.shape[1] == 1:
            sf.write(output_path, clip[:, 0], sample_rate)
        else:
            sf.write(output_path, clip, sample_rate)

        print(f"Saved {output_path.name}")
        saved_count += 1

    print(f"Done. Saved: {saved_count}")


if __name__ == "__main__":
    main()
