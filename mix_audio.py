"""Audio mixing utility that crossfades tracks once they fall below a threshold.

This script collects a list of audio files, orders them, and mixes them into a
single MP3 file. Crossfades are automatically calculated by scanning the tail
of each track and determining when the loudness drops below a user-provided
threshold.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List

from pydub import AudioSegment


def discover_audio_files(paths: Iterable[str], recursive: bool = False) -> List[Path]:
    """Return a sorted list of audio files from ``paths``.

    Directories are traversed (optionally recursively) and all files with an
    audio extension recognised by pydub/ffmpeg are returned. The resulting list
    is sorted so that playback order is deterministic.
    """

    supported_extensions = {
        ".aac",
        ".aiff",
        ".flac",
        ".m4a",
        ".mp3",
        ".ogg",
        ".wav",
        ".wma",
    }

    files: List[Path] = []
    for raw_path in paths:
        path = Path(raw_path).expanduser()
        if path.is_dir():
            if recursive:
                candidates = path.rglob("*")
            else:
                candidates = path.glob("*")
            for candidate in candidates:
                if candidate.is_file() and candidate.suffix.lower() in supported_extensions:
                    files.append(candidate)
        elif path.is_file():
            if path.suffix.lower() in supported_extensions:
                files.append(path)
            else:
                raise ValueError(f"Unsupported file extension for {path}")
        else:
            raise FileNotFoundError(f"Audio path not found: {path}")

    files.sort()
    if not files:
        raise ValueError("No audio files were discovered from the provided paths")
    return files


def safe_dbfs(segment: AudioSegment) -> float:
    """Return a finite dBFS value for a segment, treating silence as very quiet."""

    if segment.dBFS == float("-inf"):
        return -100.0
    return segment.dBFS


def compute_crossfade_duration(
    audio: AudioSegment,
    threshold_db: float,
    window_ms: int,
    minimum_crossfade_ms: int,
) -> int:
    """Compute a crossfade duration based on the tail of ``audio``.

    The tail is scanned backwards in ``window_ms`` chunks until the loudness
    rises above ``threshold_db``. The amount of time that stays below the
    threshold becomes the crossfade duration. A minimum crossfade length is
    enforced to avoid abrupt transitions when the threshold is not reached.
    """

    length_ms = len(audio)
    if length_ms == 0:
        return 0

    crossfade_ms = 0
    start = max(length_ms - window_ms, 0)
    while start >= 0:
        chunk = audio[start : start + window_ms]
        if safe_dbfs(chunk) <= threshold_db:
            crossfade_ms = length_ms - start
            start -= window_ms
        else:
            break

    crossfade_ms = max(crossfade_ms, minimum_crossfade_ms)
    return min(crossfade_ms, length_ms)


def mix_tracks(
    files: List[Path],
    threshold_db: float,
    window_ms: int,
    minimum_crossfade_ms: int,
) -> AudioSegment:
    """Return a single ``AudioSegment`` containing all tracks mixed together."""

    segments = [AudioSegment.from_file(file) for file in files]
    mixed = segments[0]
    previous_segment = segments[0]

    for next_segment in segments[1:]:
        crossfade_ms = compute_crossfade_duration(
            previous_segment,
            threshold_db=threshold_db,
            window_ms=window_ms,
            minimum_crossfade_ms=minimum_crossfade_ms,
        )
        crossfade_ms = min(crossfade_ms, len(next_segment))
        mixed = mixed.append(next_segment, crossfade=crossfade_ms)
        previous_segment = next_segment

    return mixed


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mix audio files into one MP3 with automatic crossfades.",
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Audio files or directories containing audio files. Order is alphabetical.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="mix.mp3",
        help="Destination MP3 filename (default: mix.mp3)",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=-25.0,
        help="dBFS threshold that triggers the crossfade (default: -25dB)",
    )
    parser.add_argument(
        "-w",
        "--window",
        type=int,
        default=200,
        help="Analysis window size in milliseconds (default: 200)",
    )
    parser.add_argument(
        "-m",
        "--minimum-crossfade",
        type=int,
        default=2000,
        help="Minimum crossfade duration in milliseconds (default: 2000)",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively search directories for audio files.",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)

    files = discover_audio_files(args.inputs, recursive=args.recursive)
    print(f"Discovered {len(files)} tracks to mix:")
    for file in files:
        print(f" - {file}")

    mixed = mix_tracks(
        files,
        threshold_db=args.threshold,
        window_ms=args.window,
        minimum_crossfade_ms=args.minimum_crossfade,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    mixed.export(output_path, format="mp3")
    print(f"Mixed track exported to {output_path.resolve()}")


if __name__ == "__main__":
    main()
