import base64
from email.message import EmailMessage

import yaml
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from requests import HTTPError

import google_accounts

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


def send_email(sender: str, recipient: str) -> bool:
    message = create_message()
    message["To"] = recipient
    message["From"] = sender
    try:
        send = (
            resource()
            .users()
            .messages()
            .send(
                userId=sender,
                body={"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()},
            )
            .execute()
        )
    except (HTTPError, HttpError):
        return False
    return True if "SENT" in send.get("labelIds", []) else False


if __name__ == "__main__":
    test_accounts = google_accounts.get_testing_accounts()
    with open("artifacts/predefined.yaml", "r") as yml:
        predefined = yaml.safe_load(yml)
    success = []
    failed = []
    for i, acc in enumerate(test_accounts):
        if acc in predefined["bad_accounts"]:
            continue
        to_email = test_accounts[::-1][i]
        to_email = predefined["default_recipient"] if to_email == acc else to_email

        # Print username and password pair for manual login and authorization
        print(f"Sign in with {acc} and authorize Satellite2")

        tf = lambda x: x + "@gmail.com" if not x.endswith("@gmail.com") else x
        if send_email(tf(acc), tf(to_email)):
            success.append(acc)
        else:
            failed.append(acc)

    print("++++++++++\nRESULT\n++++++++++")
    for uname in success:
        print(f"[\u2713] {uname}")
    for uname in failed:
        print(f"[\u2717] {uname}")
