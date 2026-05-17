import requests
import json
import time

from llm.prompt_builder import build_prompt

INPUT_FILE = "outputs/second_output.json"
OUTPUT_FILE = "outputs/final_output.json"

LLM_URL = "http://localhost:8080/completion"

processed_ids = set()

context_buffer = []

semantic_memory = []

MAX_MEMORY = 5


def collect_contextual_conversation(new_entry):

    global semantic_memory

    semantic_memory.append(new_entry)

    if len(semantic_memory) > MAX_MEMORY:
        semantic_memory.pop(0)

    combined_text = []

    for item in semantic_memory:
        combined_text.append(item["text"])

    return " ".join(combined_text)


def update_context(text):

    context_buffer.append(text)

    if len(context_buffer) > 5:
        context_buffer.pop(0)


def get_context():

    return " | ".join(context_buffer)


def call_llm(prompt):

    payload = {
        "prompt": prompt,
        "max_tokens": 170,
        "temperature": 0.4,
        "stop": ["###"]
    }

    response = requests.post(
        LLM_URL,
        json=payload,
        timeout=60
    )

    result = response.json()

    if "content" in result:
        return result["content"]

    if "choices" in result:
        return result["choices"][0]["text"]

    return ""


def validate_json(output):

    try:
        return json.loads(output)
    except:
        return None


def process_llm():

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

                combined_text = collect_contextual_conversation(entry)

                update_context(combined_text)

                context = get_context()

                semantic_input = {
                    "conversation": combined_text,
                    "latest_entry": entry
                }

                prompt = build_prompt(context, semantic_input)

                validated = None

                for _ in range(3):

                    output = call_llm(prompt)

                    validated = validate_json(output)

                    if validated:
                        break

                if validated:

                    validated["id"] = entry_id
                    validated["timestamp"] = entry["timestamp"]

                    try:
                        with open(OUTPUT_FILE, "r") as f:
                            existing = json.load(f)
                    except:
                        existing = []

                    existing.append(validated)

                    with open(OUTPUT_FILE, "w") as f:
                        json.dump(existing, f, indent=4)

                    print("LLM:", validated)

                processed_ids.add(entry_id)

                time.sleep(1)

        except Exception as e:
            print("LLM Error:", e)

        time.sleep(2)