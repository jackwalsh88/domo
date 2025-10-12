# Audio Crossfade Mixer

A small command-line utility that stitches together multiple audio files and
exports a single MP3. Each transition uses a crossfade that begins once the
trailing audio level falls below a configurable loudness threshold.

## Requirements

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/) (required by [pydub](https://github.com/jiaaro/pydub))
- Python dependencies: `pydub`

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python mix_audio.py <audio files or directories>
```

### Options

- `-o, --output` &mdash; Output MP3 filename (default: `mix.mp3`).
- `-t, --threshold` &mdash; dBFS threshold that triggers the crossfade (default: `-25`).
- `-w, --window` &mdash; Analysis window size in milliseconds (default: `200`).
- `-m, --minimum-crossfade` &mdash; Minimum crossfade duration in milliseconds (default: `2000`).
- `-r, --recursive` &mdash; Recursively search directories for audio files.

Example mixing the contents of a folder:

```bash
python mix_audio.py ~/music/playlist -r -o roadtrip.mp3
```

The discovered tracks are sorted alphabetically to ensure deterministic
ordering. The script prints the selected files and saves the final MP3 to the
location specified by `--output`.
