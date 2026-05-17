




from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import uuid
from datetime import datetime

MODEL_PATH = r"YOUR_VOSK_MODEL_PATH"
OUTPUT_FILE = "outputs/first_output.json"

model = Model(r"C:\Users\sanst\OneDrive\Desktop\CAVAS\model\vosk-model-small-IndianEnglish\vosk-model-small-en-in-0.4")
rec = KaldiRecognizer(model, 16000)

q = queue.Queue()


def callback(indata, frames, time, status):
    q.put(bytes(indata))



def save_output(text):

    if len(text.split()) < 2:
        return

    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": str(datetime.now()),
        "text": text
    }

    try:
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)



def run_stt():

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):

        print("🎤 Listening...")

        while True:

            data = q.get()

            if rec.AcceptWaveform(data):

                result = json.loads(rec.Result())
                text = result.get("text", "").strip().lower()

                if text:
                    print("STT:", text)
                    save_output(text)