import os
import time
import subprocess


# =====================================
# FILE PATH
# =====================================

FINAL_OUTPUT_JSON = (
    r"C:\Users\sanst\OneDrive\Desktop\CAVAS\outputs\final_output.json"
)


# =====================================
# EXECUTOR DIRECTORY
# =====================================

EXECUTOR_FOLDER = (
    r"C:\Users\sanst\OneDrive\Desktop\CAVAS\executor"
)


# =====================================
# CHECK INTERVAL
# =====================================

POLL_INTERVAL = 10


# =====================================
# LAST MODIFIED TIME
# =====================================

last_modified_time = None


print("\n================================")
print("EXECUTOR WATCHER STARTED")
print("================================")


while True:

    try:

        # =========================
        # FILE EXISTS?
        # =========================

        if not os.path.exists(FINAL_OUTPUT_JSON):

            time.sleep(POLL_INTERVAL)
            continue

        # =========================
        # GET MODIFIED TIME
        # =========================

        current_modified_time = (
            os.path.getmtime(FINAL_OUTPUT_JSON)
        )

        # =========================
        # FIRST RUN
        # =========================

        if last_modified_time is None:

            last_modified_time = (
                current_modified_time
            )

        # =========================
        # FILE UPDATED
        # =========================

        elif current_modified_time != last_modified_time:

            print("\n================================")
            print("NEW ACTION DETECTED")
            print("================================")

            last_modified_time = (
                current_modified_time
            )

            subprocess.run(

                ["python", "main.py"],

                cwd=EXECUTOR_FOLDER
            )

            print("\n[WATCHER]")
            print("Monitoring resumed")

    except Exception as e:

        print("\n[WATCHER ERROR]")
        print(str(e))

    time.sleep(POLL_INTERVAL)