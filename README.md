# Dictate 🎙️

Simple voice-to-text dictation for macOS.

## What it does

Hold right option key, speak, release - your words get transcribed and typed wherever your cursor is.

Note that if you move the cursor or change windows before transcription completes then it will be pasted wherever the cursor is upon finishing.

## Installation & Usage

```bash
git clone https://github.com/rian-dolphin/dictate.git
cd dictate
uv run src/dictate/cli.py
```

## Requirements

- uv
- Apple Silicon Mac

## Configuration

You can change the key used for activating by changing `KEY_LABEL` in the `cli.py` file.

## Credits

Forked from [VibeVoice](https://github.com/mpaepper/vibevoice), which was based on [whisper-keyboard](https://github.com/vlad-ds/whisper-keyboard) by Vlad, using [Faster Whisper](https://github.com/guillaumekln/faster-whisper).