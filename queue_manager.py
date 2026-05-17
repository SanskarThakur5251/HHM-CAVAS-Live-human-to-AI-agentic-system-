import time


def create_pending_action(

    action_store,
    action_id,
    action_data,
    expiry_seconds=60

):

    current_time = int(
        time.time()
    )

    action_store[action_id] = {

        "status": "pending_confirmation",

        "created_at": current_time,

        "expires_at": (
            current_time + expiry_seconds
        ),

        "data": action_data
    }


def is_action_expired(action):

    current_time = int(
        time.time()
    )

    return (

        current_time
        >
        action["expires_at"]

    )