"""
Pitch-preserving duration normalizer.
Reads WAV files from `INPUT_FOLDER`, stretches each clip to `TARGET_MS`
with Rubber Band, trims or pads to the exact target length, applies a volume
multiplier, then checks the normalized output files and applies edge fades only
when needed.
"""

from pathlib import Path
import subprocess

import numpy as np
import soundfile as sf


INPUT_FOLDER = "voice_neni_stress"
OUTPUT_FOLDER = "voice_neni"
TARGET_MS = 100
VOLUME_MULTIPLIER = 0.9
PITCH_SEMITONES = -2
RUBBERBAND_EXE = "rubberband-r3"
EDGE_MS = 10
FADE_MS = 10
RMS_WINDOW_MS = 1
NEEDS_FADE_SCORE = 0.05


def get_target_samples(sample_rate):
    return int(round(sample_rate * TARGET_MS / 1000.0))


def get_sample_count(sample_rate, ms):
    return int(round(sample_rate * ms / 1000.0))


def fit_to_length(audio, target_samples):
    audio = np.asarray(audio, dtype=np.float32)
    current_samples = len(audio)

    if current_samples == target_samples:
        return audio

    if current_samples > target_samples:
        return audio[:target_samples]

    if audio.ndim == 1:
        padded = np.zeros(target_samples, dtype=np.float32)
    else:
        padded = np.zeros((target_samples, audio.shape[1]), dtype=np.float32)

    padded[:current_samples] = audio
    return padded


def get_window_rms(audio, sample_rate):
    window_samples = get_sample_count(sample_rate, RMS_WINDOW_MS)
    total_windows = int(np.ceil(len(audio) / float(window_samples)))
    values = []

    for i in range(total_windows):
        start = i * window_samples
        end = min(start + window_samples, len(audio))
        window = audio[start:end]
        rms = np.sqrt(np.mean(window * window))
        values.append(rms)

    return np.asarray(values, dtype=np.float32)


def get_body_level(rms):
    body_level = np.percentile(rms, 90)

    if body_level <= 0:
        raise ValueError("Audio has no measurable RMS level.")

    return body_level


def get_fade_in_score(rms, body_level, edge_windows):
    edge = rms[:edge_windows]
    ramp = np.linspace(0.0, body_level, len(edge), dtype=np.float32)
    excess = np.maximum(0.0, edge - ramp)
    return float(np.mean(excess) / body_level)


def get_fade_out_score(rms, body_level, edge_windows):
    edge = rms[-edge_windows:]
    ramp = np.linspace(body_level, 0.0, len(edge), dtype=np.float32)
    excess = np.maximum(0.0, edge - ramp)
    return float(np.mean(excess) / body_level)


def apply_fade_in(audio, sample_rate):
    fade_samples = get_sample_count(sample_rate, FADE_MS)
    ramp = np.linspace(0.0, 1.0, fade_samples, dtype=np.float32)

    if audio.ndim > 1:
        ramp = ramp[:, np.newaxis]

    audio[:fade_samples] *= ramp


def apply_fade_out(audio, sample_rate):
    fade_samples = get_sample_count(sample_rate, FADE_MS)
    ramp = np.linspace(1.0, 0.0, fade_samples, dtype=np.float32)

    if audio.ndim > 1:
        ramp = ramp[:, np.newaxis]

    audio[-fade_samples:] *= ramp


def stretch_file(in_path, out_path):
    target_duration_seconds = TARGET_MS / 1000.0

    command = [
        RUBBERBAND_EXE,
        "--quiet",
        "--duration",
        str(target_duration_seconds),
    ]

    if PITCH_SEMITONES != 0:
        command.extend(["--pitch", str(PITCH_SEMITONES)])

    command.extend([str(in_path), str(out_path)])
    subprocess.run(command, check=True)


def fit_output_file(out_path, target_samples):
    audio, sample_rate = sf.read(out_path, always_2d=False)
    audio = fit_to_length(audio, target_samples)
    sf.write(out_path, audio, sample_rate)


def apply_volume(out_path):
    audio, sample_rate = sf.read(out_path, always_2d=False)
    audio = np.asarray(audio, dtype=np.float32)
    audio *= VOLUME_MULTIPLIER
    sf.write(out_path, audio, sample_rate)


def apply_needed_fades(out_path):
    audio, sample_rate = sf.read(out_path, always_2d=False)

    edge_samples = get_sample_count(sample_rate, EDGE_MS)
    fade_samples = get_sample_count(sample_rate, FADE_MS)

    if len(audio) < edge_samples * 2:
        raise ValueError(f"Audio is too short for {EDGE_MS} ms edge analysis: {out_path}")

    if len(audio) < fade_samples * 2:
        raise ValueError(f"Audio is too short for {FADE_MS} ms fades: {out_path}")

    rms = get_window_rms(audio, sample_rate)
    body_level = get_body_level(rms)
    edge_windows = get_sample_count(sample_rate, EDGE_MS) // get_sample_count(sample_rate, RMS_WINDOW_MS)

    fade_in_score = get_fade_in_score(rms, body_level, edge_windows)
    fade_out_score = get_fade_out_score(rms, body_level, edge_windows)
    needs_fade_in = fade_in_score >= NEEDS_FADE_SCORE
    needs_fade_out = fade_out_score >= NEEDS_FADE_SCORE

    audio = np.asarray(audio, dtype=np.float32)

    if needs_fade_in:
        apply_fade_in(audio, sample_rate)

    if needs_fade_out:
        apply_fade_out(audio, sample_rate)

    if needs_fade_in or needs_fade_out:
        sf.write(out_path, audio, sample_rate)

    return fade_in_score, needs_fade_in, fade_out_score, needs_fade_out


def process_file(in_path, out_path):
    audio, sample_rate = sf.read(in_path, always_2d=False)

    if len(audio) == 0:
        raise ValueError(f"Audio file is empty: {in_path}")

    target_samples = get_target_samples(sample_rate)
    stretch_file(in_path, out_path)
    fit_output_file(out_path, target_samples)
    print(f"Processed {in_path.name} -> {out_path.name}")
    return True


def main():
    base_folder = Path(__file__).resolve().parent
    input_folder = base_folder / INPUT_FOLDER
    output_folder = base_folder / OUTPUT_FOLDER

    if not input_folder.exists():
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    output_folder.mkdir(parents=True, exist_ok=True)

    processed_count = 0
    out_paths = []

    for in_path in sorted(input_folder.glob("*.wav")):
        out_path = output_folder / in_path.name
        process_file(in_path, out_path)
        processed_count += 1
        out_paths.append(out_path)

    for out_path in out_paths:
        apply_volume(out_path)
        print(f"{out_path.name}: volume x{VOLUME_MULTIPLIER}")

    for out_path in out_paths:
        fade_in_score, needs_fade_in, fade_out_score, needs_fade_out = apply_needed_fades(out_path)

        print(
            f"{out_path.name}: "
            f"fade in={fade_in_score:.3f} {'YES' if needs_fade_in else 'no '}  "
            f"out={fade_out_score:.3f} {'YES' if needs_fade_out else 'no '}"
        )

    print(f"Done. Processed: {processed_count}")


if __name__ == "__main__":
    main()
