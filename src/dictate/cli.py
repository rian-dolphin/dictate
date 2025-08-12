"""Command-line interface for dictation"""

import os
import subprocess
import sys
import time

import numpy as np
import requests
import sounddevice as sd
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key, Listener
from scipy.io import wavfile


def start_whisper_server():
    server_script = os.path.join(os.path.dirname(__file__), "server.py")
    process = subprocess.Popen(["python", server_script])
    return process


def wait_for_server(timeout=1800, interval=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:4242/health")
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(interval)
    raise TimeoutError("Server failed to start within timeout")


def main():
    KEY_LABEL = "alt_r"
    RECORD_KEY = Key[KEY_LABEL]
    #    CMD_KEY = KeyCode(vk=65027)  # This is how you can use non-standard keys, this is AltGr for me

    recording = False
    audio_data = []
    sample_rate = 16000
    keyboard_controller = KeyboardController()

    def on_press(key):
        nonlocal recording, audio_data
        if key == RECORD_KEY and not recording:
            recording = True
            audio_data = []
            print("Listening...")

    def on_release(key):
        nonlocal recording, audio_data
        if key == RECORD_KEY:
            recording = False
            print("Transcribing...")

            try:
                audio_data_np = np.concatenate(audio_data, axis=0)
            except ValueError as e:
                print(e)
                return

            recording_path = os.path.abspath("recording.wav")
            audio_data_int16 = (audio_data_np * np.iinfo(np.int16).max).astype(np.int16)
            wavfile.write(recording_path, sample_rate, audio_data_int16)

            try:
                response = requests.post(
                    "http://localhost:4242/transcribe/",
                    json={"file_path": recording_path},
                )
                response.raise_for_status()
                transcript = response.json()["text"]

                if transcript:
                    processed_transcript = transcript + " "
                    print(processed_transcript)
                    keyboard_controller.type(processed_transcript)
            except Exception as e:
                print(f"Error sending request to local API: {e}")
            except Exception as e:
                print(f"Error processing transcript: {e}")

    def callback(indata, frames, time, status):
        if status:
            print(status)
        if recording:
            audio_data.append(indata.copy())

    server_process = start_whisper_server()

    try:
        print("Waiting for the server to be ready...")
        wait_for_server()
        print(f"Dictation is active. Hold down {KEY_LABEL} to start dictating.")
        with Listener(on_press=on_press, on_release=on_release) as listener:
            with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
                listener.join()
    except TimeoutError as e:
        print(f"Error: {e}")
        server_process.terminate()
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        server_process.terminate()


if __name__ == "__main__":
    main()
