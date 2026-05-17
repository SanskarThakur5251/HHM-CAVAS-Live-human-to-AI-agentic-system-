import json
import uuid
import os

from validator import validate_action
from queue_manager import create_pending_action
from confirmation_manager import (
    build_confirmation_message
)
from router import execute_action


# =====================================
# MEMORY QUEUE
# =====================================

PENDING_ACTIONS = {}


# =====================================
# INPUT JSON FILE
# =====================================

JSON_FILE = (
    r"C:\Users\sanst\OneDrive\Desktop\CAVAS\outputs\final_output.json"
)


# =====================================
# PROCESS SINGLE ACTION
# =====================================

def process_action(action_data):

    # =========================
    # VALIDATION
    # =========================

    is_valid, message = validate_action(
        action_data
    )

    if not is_valid:

        print("\n[VALIDATION FAILED]")
        print(message)

        return

    # =========================
    # CREATE ACTION ID
    # =========================

    action_id = str(uuid.uuid4())

    create_pending_action(

        action_store=PENDING_ACTIONS,

        action_id=action_id,

        action_data=action_data,

        expiry_seconds=60
    )

    # =========================
    # BUILD CONFIRMATION
    # =========================

    confirmation_text = (
        build_confirmation_message(
            action_data
        )
    )

    print("\n================================")
    print("CONFIRMATION REQUIRED")
    print("================================")

    print(f"ACTION ID: {action_id}")

    print(confirmation_text)

    print("================================")

    # =========================
    # USER APPROVAL
    # =========================

    response = input(
        "Approve? (yes/no): "
    ).strip().lower()

    # =========================
    # EXECUTE ACTION
    # =========================

    if response == "yes":

        execute_action(
            action_store=PENDING_ACTIONS,
            action_id=action_id
        )

    else:

        PENDING_ACTIONS[action_id][
            "status"
        ] = "rejected"

        print("\n[INFO]")
        print("Action rejected")


# =====================================
# MAIN
# =====================================

def main():

    # =========================
    # FILE EXISTS?
    # =========================

    if not os.path.exists(JSON_FILE):

        print("\n[ERROR]")
        print("final_output.json not found")

        return

    # =========================
    # LOAD JSON SAFELY
    # =========================

    try:

        with open(
            JSON_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            actions = json.load(f)

    except json.JSONDecodeError:

        print("\n[ERROR]")
        print("Invalid or incomplete JSON")

        return

    except Exception as e:

        print("\n[ERROR]")
        print(str(e))

        return

    # =========================
    # EMPTY FILE?
    # =========================

    if not actions:

        print("\n[INFO]")
        print("No actions found")

        return

    # =========================
    # SINGLE ACTION SUPPORT
    # =========================

    if isinstance(actions, dict):

        actions = [actions]

    # =========================
    # PROCESS ACTIONS
    # =========================

    for index, action in enumerate(actions):

        print("\n")
        print("################################")
        print(f"ACTION {index + 1}")
        print("################################")

        process_action(action)


# =====================================
# ENTRY
# =====================================

if __name__ == "__main__":

    main()