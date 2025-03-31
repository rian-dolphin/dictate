"""Command-line interface for vibevoice"""

import os
import subprocess
import time
import json
import sounddevice as sd
import numpy as np
import requests
import sys

from pynput.keyboard import Controller as KeyboardController, Key, Listener, KeyCode
from scipy.io import wavfile
from dotenv import load_dotenv

from loading_indicator import LoadingIndicator

loading_indicator = LoadingIndicator()

def start_whisper_server():
    server_script = os.path.join(os.path.dirname(__file__), 'server.py')
    process = subprocess.Popen(['python', server_script])
    return process

def wait_for_server(timeout=1800, interval=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get('http://localhost:4242/health')
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(interval)
    raise TimeoutError("Server failed to start within timeout")

def _process_llm_cmd(keyboard_controller, transcript):
    """Process transcript with Ollama and type the response."""

    try:
        loading_indicator.show(message=f"Processing: {transcript}")
        
        model = os.getenv('OLLAMA_MODEL', 'gemma3:27b')
        
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": transcript.lower().strip(),
            "stream": True
        }

        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                data = line.decode('utf-8')
                if data.startswith('{'):
                    chunk = json.loads(data)
                    if 'response' in chunk:
                        keyboard_controller.type(chunk['response'])
                        
                        loading_indicator.hide()
        
        return "Successfully processed with Ollama"
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
        return "Error processing command"
    finally:
        loading_indicator.hide()

def main():
    load_dotenv()
    key_label = os.environ.get("VOICEKEY", "ctrl_r")
    RECORD_KEY = Key[key_label]
    CMD_KEY = KeyCode(vk=65027)

    recording = False
    audio_data = []
    sample_rate = 16000
    keyboard_controller = KeyboardController()

    def on_press(key):
        nonlocal recording, audio_data
        if key == RECORD_KEY or key == CMD_KEY:
            recording = True
            audio_data = []
            print("Listening...")

    def on_release(key):
        nonlocal recording, audio_data
        if key == RECORD_KEY or key == CMD_KEY:
            recording = False
            print("Transcribing...")
            
            try:
                audio_data_np = np.concatenate(audio_data, axis=0)
            except ValueError as e:
                print(e)
                return
            
            recording_path = os.path.abspath('recording.wav')
            audio_data_int16 = (audio_data_np * np.iinfo(np.int16).max).astype(np.int16)
            wavfile.write(recording_path, sample_rate, audio_data_int16)

            try:
                response = requests.post('http://localhost:4242/transcribe/', 
                                      json={'file_path': recording_path})
                response.raise_for_status()
                transcript = response.json()['text']
                
                if transcript and key == RECORD_KEY:
                    processed_transcript = transcript + " "
                    print(processed_transcript)
                    keyboard_controller.type(processed_transcript)
                elif transcript and key == CMD_KEY:
                    _process_llm_cmd(keyboard_controller, transcript)
            except requests.exceptions.RequestException as e:
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
        print(f"Waiting for the server to be ready...")
        wait_for_server()
        print(f"vibevoice is active. Hold down {key_label} to start dictating.")
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
