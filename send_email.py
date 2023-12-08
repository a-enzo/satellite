import base64
import re
from email.message import EmailMessage
from typing import Tuple

import yaml
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from requests import HTTPError

import testing_accounts

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
API_SERVICE_NAME = "gmail"
API_VERSION = "v1"


def resource() -> Resource:
    flow = InstalledAppFlow.from_client_secrets_file(
        "artifacts/client_secret.json", SCOPES
    )
    return build(
        API_SERVICE_NAME, API_VERSION, credentials=flow.run_local_server(port=0)
    )


def create_message() -> EmailMessage:
    with open("artifacts/email_body.html", "r") as f:
        body = f.read()
    message = EmailMessage()
    message.add_alternative(body, subtype="html")
    message["Subject"] = "Satellite by Drivemode QA"
    return message


def get_emails() -> Tuple:
    add_domain = lambda x: x + "@gmail.com" if not re.search(r"@gmail.com", x) else x
    tmp = next(iter(google_accounts[::-1][i]))  # temporary recipient
    _sender = next(iter(account))
    _recipient = tmp if tmp != _sender else predefined["default_recipient"]
    return add_domain(_sender), add_domain(_recipient)


def send_email(_sender: str, _recipient: str) -> bool:
    message = create_message()
    message["To"] = _recipient
    message["From"] = _sender
    try:
        send = (
            resource()
            .users()
            .messages()
            .send(
                userId=_sender,
                body={"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()},
            )
            .execute()
        )
    except (HTTPError, HttpError):
        return False
    return True if "SENT" in send.get("labelIds", []) else False


if __name__ == "__main__":
    google_accounts = testing_accounts.testing_accounts()
    with open("artifacts/predefined.yaml", "r") as yml:
        predefined = yaml.safe_load(yml)
    success = []
    failed = []
    for i, account in enumerate(google_accounts):
        sender, recipient = get_emails()
        if sender in predefined["bad_accounts"]:
            continue

        # Print username and password pair for manual login and authorization
        print(f"Sign in with {sender} and authorize Satellite2")

        if send_email(sender, recipient):
            success.append(sender)
        else:
            failed.append(sender)

    print("++++++++++\nRESULT\n++++++++++")
    for uname in success:
        print(f"[\u2713] {uname}")
    for uname in failed:
        print(f"[\u2717] {uname}")
