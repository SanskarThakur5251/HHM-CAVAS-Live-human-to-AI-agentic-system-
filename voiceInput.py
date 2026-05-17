from vosk import Model, KaldiRecognizer
import pyaudio
import json
from datetime import datetime

# Load model
model = Model(r"C:\Users\sanst\OneDrive\Desktop\CAVAS\model\vosk-model-small-IndianEnglish\vosk-model-small-en-in-0.4")

recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()

stream = mic.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    input_device_index=2,   # 👈 set correct index
    frames_per_buffer=8192
)

stream.start_stream()

print("🎤 Listening...")

# Save function
def save_to_json(text):
    entry = {
        "timestamp": str(datetime.now()),
        "text": text
    }

    try:
        with open("speech_data.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open("speech_data.json", "w") as f:
        json.dump(data, f, indent=4)

# Main loop
while True:
    data = stream.read(4096, exception_on_overflow=False)

    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "").strip()

        if text:
            print("📝 Final:", text)
            save_to_json(text)

            if "stop listening" in text.lower():
                print("🛑 Stopping...")
                break
    else:
        partial = json.loads(recognizer.PartialResult())
        print("🔹 Partial:", partial.get("partial", ""))