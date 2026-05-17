1. Project Overview

CAVAS (Context-Aware Voice Automation System) is an AI-based voice assistant architecture designed to continuously listen to user speech, convert spoken language into text, understand conversational meaning, identify actionable information, and eventually execute real-world actions such as creating reminders, storing notes, scheduling events, and interacting with productivity tools.

The system is designed using a modular pipeline architecture where each layer performs a specific task independently and passes structured data to the next layer through JSON interfaces.

Current uploaded repository version contains the Speech-to-Text (STT) pipeline and foundational processing framework.

Planned future stages:

Semantic understanding layer
Context management
Local LLM reasoning
Action executor layer
Gmail integration
Google Calendar integration
Note generation
Offline-first synchronization system
2. Current Workflow Architecture
User Voice
      ↓
Microphone Stream
      ↓
Vosk Speech-to-Text Model
      ↓
Text Extraction
      ↓
JSON Generation
      ↓
first_output.json
      ↓
Semantic Intelligence Layer
      ↓
Contextual Understanding
      ↓
LLM Reasoning Layer
      ↓
Structured Action JSON
      ↓
Executor Layer
      ↓
External APIs
3. Detailed Current Pipeline Flow
Stage 1: Voice Capture

The microphone continuously captures real-time audio input from the user.

The audio stream:

operates continuously
uses raw audio chunks
processes streaming audio
minimizes latency

Technology:

sounddevice

Purpose:

Real-time microphone stream acquisition
Stage 2: Speech Recognition

Captured audio enters the Vosk Speech Recognition Model.

Responsibilities:

convert speech to text
support offline transcription
process audio in real time
avoid cloud dependency

Technology:

Vosk
KaldiRecognizer

Model used:

vosk-model-small-en-in-0.4

Characteristics:

Indian English optimized
fully offline
lightweight
CPU efficient

Output example:

{
   "text":"schedule meeting tomorrow at five"
}
Stage 3: JSON Output Generation

Recognized speech is stored in structured JSON format.

Example:

[
   {
      "id":"uuid",
      "timestamp":"2026-05-17 12:30:05",
      "text":"schedule meeting tomorrow at five"
   }
]

Purpose:

persistent storage
debugging
pipeline communication
modular architecture

Output file:

outputs/first_output.json
4. Repository Structure

Current repository structure:

CAVAS/
│
├── voice/
│      └── stt.py
│
├── semantic/
│      ├── semantic_model.py
│      └── labels.json
│
├── llm/
│      ├── llm_client.py
│      └── prompt_builder.py
│
├── utils/
│      ├── context_manager.py
│      └── json_utils.py
│
├── Main_Pipeline.py
├── mic.py
├── voiceInput.py
├── requirements.txt
├── .gitignore
└── speech_data.json
5. File-by-File Explanation
Main_Pipeline.py

Purpose:

Main controller of the system.

Responsibilities:

starts all modules
manages threads
keeps pipeline alive
controls system execution flow
voice/stt.py

Purpose:

Speech Recognition Engine

Responsibilities:

microphone initialization
audio chunk processing
Vosk inference
output generation
semantic/semantic_model.py

Purpose:

Semantic preprocessing layer

Responsibilities:

receives STT output
analyzes sentence meaning
predicts semantic tags
creates structured contextual data

Future responsibilities:

detect intent
identify entities
classify actionability
determine priorities
semantic/labels.json

Purpose:

Stores semantic labels.

Examples:

{
"create_event":0,
"save_note":1,
"question":2
}
llm/llm_client.py

Purpose:

Local LLM communication engine.

Responsibilities:

communicate with llama.cpp server
send prompts
receive responses
validate generated output
llm/prompt_builder.py

Purpose:

Prompt engineering module.

Responsibilities:

build structured prompts
inject context
maintain response format
utils/context_manager.py

Purpose:

Context storage engine.

Responsibilities:

maintain conversation history
provide rolling context window
utils/json_utils.py

Purpose:

Utility helper functions.

Responsibilities:

JSON read/write
validation
formatting
6. Files Not Uploaded to GitHub

The following files are intentionally excluded.

Vosk Speech Models

Examples:

vosk-model-small-en-in-0.4
vosk-model-en-in-0.5

Reason:

Large file size

Purpose:

Speech recognition inference

Approximate size:

50–200MB+
LLM Models

Examples:

Qwen3.gguf
Mistral.gguf

Reason:

Extremely large

Purpose:

Local language reasoning

Approximate size:

2–8GB+
Semantic Model Files

Examples:

model.safetensors
config.json
tokenizer.json

Reason:

Large training artifacts

Purpose:

Semantic understanding
Virtual Environment

Example:

venv/

Reason:

Machine specific

Contains:

installed packages
binaries
Python dependencies
Generated Output Files

Examples:

first_output.json
second_output.json
final_output.json

Reason:

Runtime generated data

Purpose:

debugging
execution logs
7. Technologies Used
Technology	Purpose
Python	Core implementation language
Vosk	Offline Speech Recognition
KaldiRecognizer	Speech decoding
sounddevice	Microphone stream processing
Transformers	Semantic model inference
PyTorch	Deep learning backend
llama.cpp	Local LLM inference
JSON	Inter-module communication
Threading	Concurrent execution
UUID	Unique message tracking
Git	Version control
GitHub	Repository hosting
8. Current Features

Implemented:

✅ Real-time microphone listening
✅ Offline speech recognition
✅ JSON output generation
✅ Modular architecture
✅ Threaded execution
✅ Local execution support
✅ Scalable pipeline structure

Future:

⬜ Semantic tagging
⬜ Context management
⬜ LLM reasoning
⬜ Gmail automation
⬜ Calendar integration
⬜ Notes generation
⬜ Task execution engine
⬜ Offline synchronization

9. Scalability Design

The architecture follows a modular design:

Voice
↓
Semantic Layer
↓
Reasoning Layer
↓
Executor Layer

Advantages:

independent module updates
easier debugging
low coupling
scalable design
replaceable AI components

1. Main_Pipeline.py

This is the master controller.

Think of this as the operating system of your project.

It does not perform AI processing itself.

Its job is:

start all modules
create threads
keep the system running
shut down safely
Script structure

Example:

import threading

from voice.stt import run_stt
from semantic.semantic_model import process_pipeline
from llm.llm_client import process_llm
What happens internally
Step 1

Imports all modules

STT module
Semantic module
LLM module
Step 2

Creates independent threads:

stt_thread = threading.Thread(
    target=run_stt,
    daemon=True
)
Why threads?

Without threads:

STT waits for semantic model
Semantic waits for LLM

Very slow.

With threads:

STT → running
Semantic → running
LLM → running

all simultaneously.

Output

No file generated.

Purpose:

Control system execution
2. voice/stt.py

This is your speech recognition engine.

Purpose:

Voice → Text
Major components
A. Vosk model loading
model = Model(MODEL_PATH)

What happens:

Load speech recognition model
↓
Load acoustic model
↓
Load language model
↓
Prepare decoder
B. Microphone initialization
sd.RawInputStream()

Purpose:

Open microphone stream
C. Callback function
def callback(indata):

Purpose:

Receive microphone chunks

Audio arrives continuously:

chunk1
chunk2
chunk3
chunk4
D. Queue
q.put(bytes(indata))

Purpose:

Store audio safely before processing.

Without queue:

Audio loss

may happen.

E. Speech recognition
rec.AcceptWaveform(data)

Purpose:

Convert audio:

waveform
↓
tokens
↓
words
↓
sentence
F. Save JSON
save_output(text)

Generates:

[
  {
    "id":"uuid",
    "timestamp":"2026-05-17",
    "text":"schedule meeting tomorrow"
  }
]

Saved in:

outputs/first_output.json
3. semantic/semantic_model.py

Purpose:

Text → semantic understanding

This is your middle intelligence layer.

Input:
first_output.json

Example:

{
 "text":"schedule meeting tomorrow"
}
Major sections
A. Load model
AutoModelForSequenceClassification

Purpose:

Load .safetensors

B. Load tokenizer
AutoTokenizer

Purpose:

Convert text:

schedule meeting

into:

[154,92,201]
C. Context buffer

You changed architecture to:

last 3 sentences

So internally:

conversation_buffer=[]

Example:

Sentence history:

Rahul called
Schedule meeting
Tomorrow at 5

Combined:

Rahul called Schedule meeting Tomorrow at 5
D. Model inference
outputs=model(**inputs)

Internal process:

Text
↓
Embeddings
↓
Transformer layers
↓
Classification head
↓
Semantic prediction
E. Confidence calculation
softmax()

Example:

create_event=0.88
save_note=0.09
casual=0.03
F. Save output

Creates:

{
"id":"123",
"text":"schedule meeting tomorrow",
"intent":"create_event",
"confidence":0.88,
"actionable":true
}

Saved:

outputs/second_output.json
4. semantic/labels.json

Purpose:

Maps labels to numbers.

Example:

{
"create_event":0,
"save_note":1,
"casual":2
}

Why?

Model internally predicts:

2

Not:

casual

labels.json converts:

2 → casual
5. llm/prompt_builder.py

Purpose:

Generate prompt sent to LLM.

Input:

{
"conversation":"Schedule meeting tomorrow"
}

Output:

### SYSTEM:

You are a strict AI automation engine.

Convert input to executable JSON.

Purpose:

define LLM behavior
maintain response format
reduce hallucinations
6. llm/llm_client.py

Purpose:

Semantic output → LLM reasoning
Major components
A. Read second_output.json

Input:

{
"intent":"create_event"
}
B. Memory creation

You updated architecture:

semantic_memory=[]

Purpose:

Store:

last few semantic sentences
C. Build conversation

Creates:

Schedule meeting tomorrow at 5
D. Create prompt
prompt=build_prompt()
E. Send request
requests.post(
"http://localhost:8080/completion"
)

Purpose:

Send data to:

llama.cpp server
F. Receive response

Example:

{
"intent":"create_event",
"entities":{
"title":"meeting",
"time":"5 PM"
}
}
G. Validate JSON

Purpose:

Prevent malformed output.

H. Save result

Saved:

outputs/final_output.json
7. utils/context_manager.py

Purpose:

Store conversation memory.

Example:

history=[
"Rahul called",
"Schedule meeting"
]

Purpose:

Maintain context.

8. utils/json_utils.py

Purpose:

Common helper functions.

Examples:

read_json()

write_json()

append_json()

Purpose:

Avoid duplicated code.

9. mic.py

Purpose:

Microphone testing utility.

Used for:

testing microphone
checking audio input
debugging
10. voiceInput.py

Purpose:

Earlier standalone STT testing script.

Used before full pipeline integration.

JSON Flow Through System
First output
{
"id":"1",
"text":"schedule meeting"
}

↓

Second output
{
"id":"1",
"text":"schedule meeting",
"intent":"create_event"
}

↓

Final output
{
"id":"1",
"intent":"create_event",
"entities":{
"time":"tomorrow"
}
}
Complete Runtime Timeline
0 ms:
User speaks

100–300 ms:
Vosk transcribes

400–800 ms:
Semantic model processes

1–2 sec:
LLM reasoning

2–3 sec:
Executor performs action
