import base64
import json
from email.message import EmailMessage

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError

import google_accounts


def service_account_login():
    scopes = ["https://www.googleapis.com/auth/gmail.send"]
    api_service_name = "gmail"
    api_version = "v1"
    app_flow = InstalledAppFlow.from_client_secrets_file(
        "./artifacts/credentials.json", scopes
    )
    return build(
        api_service_name, api_version, credentials=app_flow.run_local_server(port=0)
    )


def create_message(sender: str, to: str):
    """Create a message for an email.
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
    Returns:
      An object containing a base64url encoded email object.
    """
    with open("artifacts/email_body.html", "r") as f:
        body = f.read()
    email_message = EmailMessage()
    email_message.add_alternative(body, subtype="html")
    email_message["To"] = to
    email_message["From"] = sender
    email_message["Subject"] = "Satellite by Drivemode QA"
    return {"raw": base64.urlsafe_b64encode(email_message.as_bytes()).decode()}


def send_email(service, user_id, message):
    """Send an email message.
    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address.
      message: Message to be sent.
    """
    try:
        sent = (
            service.users()
            .messages()
            .send(
                userId=user_id,
                body=message,
            )
            .execute()
        )
        print(f"{user_id}: {sent}")
    except (HTTPError, HttpError) as error:
        print(json.loads(error.content)["error"]["errors"][0]["message"])


if __name__ == "__main__":
    testing_accounts = google_accounts.testing_accounts()
    for acc in testing_accounts:
        print(f"Sign in with {acc} and authorize Satellite2.")
        service = service_account_login()
        message = create_message(acc, google_accounts.email_to())
        send_email(service, acc, message)
