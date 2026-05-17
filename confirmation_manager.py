def build_confirmation_message(data):

    intent = data["intent"]

    entities = data["entities"]

    if intent == "draft_mail":

        return f"""

Draft Email

To:
{entities.get("recipient")}

Subject:
{entities.get("title")}

Content:
{entities.get("content")}
"""

    elif intent == (
        "create_calendar_event"
    ):

        return f"""

Create Calendar Event

Title:
{entities.get("title")}

Date:
{entities.get("date")}

Time:
{entities.get("time")}

Description:
{entities.get("content")}
"""

    elif intent == "create_note":

        return f"""

Create Local Note

Title:
{entities.get("title")}

Content:
{entities.get("content")}
"""

    elif intent == "update_note":

        return f"""

Update Local Note

Title:
{entities.get("title")}

New Content:
{entities.get("content")}
"""

    return "Unknown action"