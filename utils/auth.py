import os.path

from google.auth.transport.requests import (
    Request
)

from google.oauth2.credentials import (
    Credentials
)

from google_auth_oauthlib.flow import (
    InstalledAppFlow
)


SCOPES = [

    "https://www.googleapis.com/auth/gmail.compose",

    "https://www.googleapis.com/auth/calendar"

]


TOKEN_PATH = (
    "credentials/token.json"
)

CREDENTIALS_PATH = (

    "credentials/credentials.json"

)


def authenticate_google():

    creds = None

    if os.path.exists(
        TOKEN_PATH
    ):

        creds = (

            Credentials
            .from_authorized_user_file(

                TOKEN_PATH,

                SCOPES
            )
        )

    if (

        not creds

        or

        not creds.valid

    ):

        if (

            creds
            and
            creds.expired
            and
            creds.refresh_token

        ):

            creds.refresh(
                Request()
            )

        else:

            flow = (

                InstalledAppFlow
                .from_client_secrets_file(

                    CREDENTIALS_PATH,

                    SCOPES
                )
            )

            creds = (
                flow.run_local_server(
                    port=0
                )
            )

        with open(
            TOKEN_PATH,
            "w"
        ) as token:

            token.write(
                creds.to_json()
            )

    return creds