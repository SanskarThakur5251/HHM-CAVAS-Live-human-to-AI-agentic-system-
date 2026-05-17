import os


NOTES_FOLDER = "notes"

os.makedirs(
    NOTES_FOLDER,
    exist_ok=True
)


def normalize_filename(title):

    return (

        title
        .strip()
        .lower()
        .replace(
            " ",
            "_"
        )

    )


def create_note(
    entities
):

    title = entities.get(
        "title"
    )

    content = entities.get(
        "content"
    )

    filename = (

        normalize_filename(
            title
        )

        + ".md"

    )

    filepath = (
        os.path.join(
            NOTES_FOLDER,
            filename
        )
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            content
        )

    return {

        "service":
        "local_notes",

        "action":
        "note_created",

        "file":
        filepath
    }


def update_note(
    entities
):

    title = entities.get(
        "title"
    )

    content = entities.get(
        "content"
    )

    filename = (

        normalize_filename(
            title
        )

        + ".md"

    )

    filepath = (
        os.path.join(
            NOTES_FOLDER,
            filename
        )
    )

    if not os.path.exists(
        filepath
    ):

        raise Exception(
            "Note not found"
        )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            content
        )

    return {

        "service":
        "local_notes",

        "action":
        "note_updated",

        "file":
        filepath
    }