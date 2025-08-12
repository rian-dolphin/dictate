# Vibevoice 🎙️

Hi, I'm [Marc Päpper](https://x.com/mpaepper) and I wanted to vibe code like [Karpathy](https://x.com/karpathy/status/1886192184808149383) ;D, so I looked around and found the cool work of [Vlad](https://github.com/vlad-ds/whisper-keyboard). I extended it to run with a local whisper model, so I don't need to pay for OpenAI tokens.
I hope you have fun with it!

## What it does 🚀

![Demo Video](docs/vibevoice-demo-caption.gif)

Simply run `cli.py` and start dictating text anywhere in your system:
1. Hold down right control key (Ctrl_r)
2. Speak your text
3. Release the key
4. Watch as your spoken words are transcribed and automatically typed!

Works in any application or window - your text editor, browser, chat apps, anywhere you can type!


## Installation 🛠️

```bash
git clone https://github.com/mpaepper/vibevoice.git
cd vibevoice
pip install -r requirements.txt
python src/vibevoice/cli.py
```

## Requirements 📋

### Python Dependencies
- Python 3.12 or higher

### System Requirements
- CUDA-capable GPU (recommended) -> in server.py you can enable cpu use
- CUDA 12.x
- cuBLAS
- cuDNN 9.x


#### macOS Requirements

* CUDA-capable GPU recommended for best performance
* For CPU-only mode, modify server.py accordingly

## Usage 💡

1. Start the application:
```bash
python src/vibevoice/cli.py
```

2. Hold down right control key (Ctrl_r) while speaking
3. Release to transcribe
4. Your text appears wherever your cursor is!

### Configuration

You can customize various aspects of VibeVoice with the following environment variables:

#### Keyboard Controls
- `VOICEKEY`: Change the dictation activation key (default: "ctrl_r")
  ```bash
  export VOICEKEY="ctrl"  # Use left control instead
  ```



## Usage 💡

VibeVoice provides simple dictation:

1. Hold down the dictation key (default: right Control)
2. Speak your text
3. Release to transcribe
4. Your text appears wherever your cursor is!

## Credits 🙏

- Original inspiration: [whisper-keyboard](https://github.com/vlad-ds/whisper-keyboard) by Vlad
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper) for the optimized Whisper implementation
- Built by [Marc Päpper](https://www.paepper.com)
