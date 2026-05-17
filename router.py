from queue_manager import (
    is_action_expired
)

from executors.gmail_executor import (
    draft_email
)

from executors.calendar_executor import (
    create_event
)

from executors.notes_executor import (
    create_note,
    update_note
)


def execute_action(
    action_store,
    action_id
):

    action = (
        action_store[action_id]
    )

    if is_action_expired(
        action
    ):

        print(
            "\nAction expired"
        )

        return

    data = action["data"]

    intent = data["intent"]

    entities = (
        data["entities"]
    )

    if intent == "draft_mail":

        result = (
            draft_email(
                entities
            )
        )

    elif intent == (
        "create_calendar_event"
    ):

        result = (
            create_event(
                entities
            )
        )

    elif intent == (
        "create_note"
    ):

        result = (
            create_note(
                entities
            )
        )

    elif intent == (
        "update_note"
    ):

        result = (
            update_note(
                entities
            )
        )

    else:

        raise Exception(
            "Unknown intent"
        )

    print(
        "\n[SUCCESS]"
    )

    print(result)