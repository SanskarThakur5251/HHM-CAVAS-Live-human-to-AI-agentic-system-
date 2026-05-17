import threading
import time

from voice.stt import run_stt
from semantic.semantic_model import process_pipeline
from llm.llm_client import process_llm


stt_thread = threading.Thread(
    target=run_stt,
    daemon=True
)

semantic_thread = threading.Thread(
    target=process_pipeline,
    daemon=True
)

llm_thread = threading.Thread(
    target=process_llm,
    daemon=True
)


stt_thread.start()
semantic_thread.start()
llm_thread.start()


print("✅ CAVAS Pipeline Running")
print("Press Ctrl+C to stop")


try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("🛑 Shutting down pipeline...")