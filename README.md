# Vibevoice 🎙️

Hi, I'm [Marc Päpper](https://x.com/mpaepper) and I wanted to vibe code like [Karpathy](https://x.com/karpathy/status/1886192184808149383) ;D, so I looked around and found the cool work of [Vlad](https://github.com/vlad-ds/whisper-keyboard). I extended it to run with a local whisper model, so I don't need to pay for OpenAI tokens.
I hope you have fun with it!

## What it does 🚀

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

#### Handling the CUDA requirements

* Make sure that you have CUDA >= 12.4 and cuDNN >= 9.x
* I had some trouble at first with Ubuntu 24.04, so I did the following:

```bash
sudo apt update && sudo apt upgrade
sudo apt autoremove nvidia* --purge
ubuntu-drivers devices
sudo ubuntu-drivers autoinstall
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb && sudo apt update
sudo apt install cuda-toolkit-12-8
```

* Then after rebooting, it worked well.

## Usage 💡

1. Start the application:
```bash
vibevoice
```

2. Hold down right control key (Ctrl_r) while speaking
3. Release to transcribe
4. Your text appears wherever your cursor is!

### Configuration

You can customize the trigger key by setting the `VOICEKEY` environment variable:
```bash
export VOICEKEY="ctrl_l"  # Use left control instead
```

## Credits 🙏

- Original inspiration: [whisper-keyboard](https://github.com/vlad-ds/whisper-keyboard) by Vlad
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper) for the optimized Whisper implementation
- Built by [Marc Päpper](https://www.paepper.com)