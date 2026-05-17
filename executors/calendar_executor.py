from googleapiclient.discovery import build

from utils.auth import authenticate_google


def create_event(entities):

    creds = authenticate_google()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    title = entities.get("title")

    date = entities.get("date")

    time = entities.get("time")

    content = entities.get(
        "content",
        ""
    )

    # =========================
    # SIMPLE TIME HANDLING
    # =========================

    start_datetime = f"{date}T15:00:00"

    end_datetime = f"{date}T16:00:00"

    event = {

        "summary": title,

        "description": content,

        "start": {

            "dateTime": start_datetime,

            "timeZone": "Asia/Kolkata"
        },

        "end": {

            "dateTime": end_datetime,

            "timeZone": "Asia/Kolkata"
        }
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return {

        "service": "calendar",

        "action": "event_created",

        "event_id": created_event["id"]
    }