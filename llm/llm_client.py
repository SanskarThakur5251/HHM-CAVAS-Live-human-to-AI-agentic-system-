import requests
import json
import time
import re

from llm.prompt_builder import build_prompt

INPUT_FILE = r"outputs/second_output.json"
OUTPUT_FILE = r"outputs/final_output.json"

LLM_URL = "http://localhost:8080/completion"

processed_ids = set()

semantic_memory = []

MAX_MEMORY = 5


# ===============================
# CONTEXT MEMORY
# ===============================

def collect_contextual_conversation(new_entry):

    global semantic_memory

    semantic_memory.append(new_entry)

    if len(semantic_memory) > MAX_MEMORY:
        semantic_memory.pop(0)

    combined = []

    for item in semantic_memory:
        combined.append(item["text"])

    return " ".join(combined)


# ===============================
# CALL LLAMA SERVER
# ===============================

def call_llm(prompt):

    payload = {
        "prompt": prompt,
        "max_tokens": 120,
        "temperature": 0.1,
        "stop": ["###"]
    }

    try:

        response = requests.post(
            LLM_URL,
            json=payload,
            timeout=60
        )

        result = response.json()

        print("\n===== RAW SERVER RESPONSE =====")
        print(result)

        if "content" in result:
            return result["content"]

        elif "choices" in result:
            return result["choices"][0]["text"]

        return ""

    except Exception as e:

        print("\nLLM Connection Error:")
        print(e)

        return ""


# ===============================
# JSON EXTRACTION
# ===============================

def validate_json(output):

    try:

        match = re.search(
            r'\{.*\}',
            output,
            re.DOTALL
        )

        if match:

            extracted = match.group()

            print("\nExtracted JSON:")
            print(extracted)

            return json.loads(extracted)

    except Exception as e:

        print("\nJSON Validation Error:")
        print(e)

    return None


# ===============================
# SAVE OUTPUT
# ===============================

def save_output(data):

    try:

        with open(
            OUTPUT_FILE,
            "r"
        ) as f:

            existing = json.load(f)

    except:

        existing = []

    existing.append(data)

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            existing,
            f,
            indent=4
        )

    print("\nSaved to final_output.json")


# ===============================
# MAIN LOOP
# ===============================

def process_llm():

    global processed_ids

    print("\nLLM module started...\n")

    while True:

        try:

            with open(
                INPUT_FILE,
                "r"
            ) as f:

                data = json.load(f)

            for entry in data:

                if "id" not in entry:

                    print(
                        "Skipping old entry"
                    )

                    continue

                entry_id = entry["id"]

                if entry_id in processed_ids:
                    continue


                print(
                    "\n========================"
                )

                print(
                    "New Semantic Entry:"
                )

                print(entry)


                combined_text = collect_contextual_conversation(
                    entry
                )

                print(
                    "\nConversation Context:"
                )

                print(
                    combined_text
                )


                semantic_input = {

                    "conversation":
                    combined_text,

                    "latest_entry":
                    entry
                }


                prompt = build_prompt(
                    "",
                    semantic_input
                )

                print(
                    "\nPrompt Sent:"
                )

                print(
                    prompt[:500]
                )


                validated = None


                for attempt in range(3):

                    print(
                        f"\nAttempt {attempt+1}"
                    )

                    output = call_llm(
                        prompt
                    )

                    print(
                        "\nLLM Output:"
                    )

                    print(
                        output
                    )

                    validated = validate_json(
                        output
                    )

                    if validated:

                        break


                if validated:

                    validated[
                        "id"
                    ] = entry_id

                    validated[
                        "timestamp"
                    ] = entry[
                        "timestamp"
                    ]


                    print(
                        "\nValidated Output:"
                    )

                    print(
                        validated
                    )


                    save_output(
                        validated
                    )

                else:

                    print(
                        "\nCould not generate valid JSON"
                    )


                processed_ids.add(
                    entry_id
                )

            time.sleep(
                0.2
            )

        except Exception as e:

            print(
                "\nLLM Error:"
            )

            print(
                e
            )

            time.sleep(
                1
            )