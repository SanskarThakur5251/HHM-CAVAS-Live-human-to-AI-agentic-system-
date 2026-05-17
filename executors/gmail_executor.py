import base64

from email.mime.text import MIMEText

from googleapiclient.discovery import build

from utils.auth import authenticate_google


def draft_email(entities):

    creds = authenticate_google()

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    recipient = entities.get("recipient")

    subject = entities.get(
        "title",
        "No Subject"
    )

    content = entities.get("content")

    # =========================
    # EMAIL MESSAGE
    # =========================

    message = MIMEText(content)

    message["to"] = recipient

    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    body = {

        "message": {
            "raw": raw_message
        }
    }

    draft = service.users().drafts().create(
        userId="me",
        body=body
    ).execute()

    return {

        "service": "gmail",

        "action": "draft_created",

        "draft_id": draft["id"]
    }