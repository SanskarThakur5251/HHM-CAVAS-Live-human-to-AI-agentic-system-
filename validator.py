REQUIRED_FIELDS = {

    "draft_mail": [
        "recipient",
        "content"
    ],

    "create_calendar_event": [
        "title",
        "date",
        "time"
    ],

    "create_note": [
        "title",
        "content"
    ],

    "update_note": [
        "title",
        "content"
    ]
}


def validate_action(data):

    if "intent" not in data:

        return False, "Missing intent"

    if "entities" not in data:

        return False, "Missing entities"

    intent = data["intent"]

    entities = data["entities"]

    if intent not in REQUIRED_FIELDS:

        return False, (
            f"Unknown intent: {intent}"
        )

    for field in REQUIRED_FIELDS[intent]:

        value = entities.get(field)

        if value is None or value == "":

            return False, (
                f"Missing field: {field}"
            )

    return True, "Validation passed"