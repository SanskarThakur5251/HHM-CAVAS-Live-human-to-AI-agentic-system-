from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import json
import time

MODEL_PATH = r"C:\BERT_trainer\context_model"

INPUT_FILE = "outputs/first_output.json"
OUTPUT_FILE = "outputs/second_output.json"

CONFIDENCE_THRESHOLD = 0.55


tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)


label_map = {
    0: "send_email",
    1: "create_event",
    2: "create_task",
    3: "save_note",
    4: "casual",
    5: "query"
}


processed_ids = set()

conversation_buffer = []



def get_contextual_input(new_text):

    global conversation_buffer

    conversation_buffer.append(new_text)

    if len(conversation_buffer) > 3:
        conversation_buffer.pop(0)

    return " ".join(conversation_buffer)



def classify(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits

    probabilities = F.softmax(logits, dim=1)

    prediction = torch.argmax(probabilities, dim=1).item()

    confidence = torch.max(probabilities).item()

    intent = label_map[prediction]

    actionable = intent not in ["casual"]

    return {
        "text": text,
        "intent": intent,
        "actionable": actionable,
        "requires_context": False,
        "priority": "medium",
        "confidence": round(confidence, 2)
    }



def process_pipeline():

    global processed_ids

    while True:

        try:

            with open(INPUT_FILE, "r") as f:
                data = json.load(f)

            for entry in data:

                if "id" not in entry:
                    print("Skipping old entry without ID")
                    continue

                entry_id = entry["id"]

                if entry_id in processed_ids:
                    continue

                contextual_text = get_contextual_input(entry["text"])

                result = classify(contextual_text)

                result["raw_text"] = entry["text"]

                if result["confidence"] < CONFIDENCE_THRESHOLD:
                    processed_ids.add(entry_id)
                    continue

                print("Semantic:", result)

                result["id"] = entry_id
                result["timestamp"] = entry["timestamp"]

                try:
                    with open(OUTPUT_FILE, "r") as f:
                        existing = json.load(f)
                except:
                    existing = []

                existing.append(result)

                with open(OUTPUT_FILE, "w") as f:
                    json.dump(existing, f, indent=4)

                processed_ids.add(entry_id)

        except Exception as e:
            print("Semantic Error:", e)

        time.sleep(2)