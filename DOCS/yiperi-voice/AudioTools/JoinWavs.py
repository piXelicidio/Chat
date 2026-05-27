"""
Fixed-start WAV joiner.
Reads all WAV files from `SOURCE_FOLDER`, sorts them by name, places each clip
so its start is exactly `START_INTERVAL_MS` after the previous start, and saves
one joined WAV beside this script.
"""

from pathlib import Path

import numpy as np
import soundfile as sf


SOURCE_FOLDER = "voice_wiwi\\stress"
START_INTERVAL_MS = 1000


def get_start_samples(sample_rate):
    return int(round(sample_rate * START_INTERVAL_MS / 1000.0))


def to_2d(audio):
    if audio.ndim == 1:
        return audio[:, np.newaxis]

    return audio


def load_clips(input_folder):
    wav_paths = sorted(input_folder.glob("*.wav"), key=lambda path: path.name)

    if not wav_paths:
        print(f"No .wav files found in {input_folder}")
        return None, None, None

    clips = []
    sample_rate = None
    channel_count = None

    for wav_path in wav_paths:
        audio, current_sample_rate = sf.read(wav_path, always_2d=False)

        if len(audio) == 0:
            print(f"Skipped empty file: {wav_path.name}")
            continue

        audio = np.asarray(audio, dtype=np.float32)
        audio = to_2d(audio)

        current_channel_count = audio.shape[1]

        if sample_rate is None:
            sample_rate = current_sample_rate
            channel_count = current_channel_count
        elif current_sample_rate != sample_rate:
            raise ValueError(
                f"Sample rate mismatch in {wav_path.name}: "
                f"{current_sample_rate} != {sample_rate}"
            )
        elif current_channel_count != channel_count:
            raise ValueError(
                f"Channel count mismatch in {wav_path.name}: "
                f"{current_channel_count} != {channel_count}"
            )

        clips.append((wav_path.name, audio))

    if not clips:
        print(f"No valid .wav files found in {input_folder}")
        return None, None, None

    return clips, sample_rate, channel_count


def build_joined_audio(clips, sample_rate, channel_count):
    start_samples = get_start_samples(sample_rate)
    total_samples = 0

    for index, (_, audio) in enumerate(clips):
        clip_end = index * start_samples + len(audio)
        if clip_end > total_samples:
            total_samples = clip_end

    joined = np.zeros((total_samples, channel_count), dtype=np.float32)

    for index, (name, audio) in enumerate(clips):
        start = index * start_samples
        end = start + len(audio)
        joined[start:end, :] += audio
        print(f"Placed {name} at {index * START_INTERVAL_MS} ms")

    if channel_count == 1:
        return joined[:, 0]

    return joined


def main():
    base_folder = Path(__file__).resolve().parent
    input_folder = base_folder / SOURCE_FOLDER
    output_path = base_folder / f"{input_folder.name}_joined.wav"

    if not input_folder.exists():
        print(f"Source folder not found: {input_folder}")
        return

    clips, sample_rate, channel_count = load_clips(input_folder)
    if clips is None:
        return

    joined = build_joined_audio(clips, sample_rate, channel_count)
    sf.write(output_path, joined, sample_rate)

    print(f"Saved {output_path.name}")


if __name__ == "__main__":
    main()
