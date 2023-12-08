import os
import re

import yaml

TESTING_ACCOUNTS = os.environ["TESTING_ACCOUNTS"]


def is_gmail_account(account: dict) -> bool:
    try:
        if re.search(r"Google", account["name"]):
            return True
    except KeyError:
        return False


def testing_accounts():
    return [
        {account["login"]["username"]: account["login"]["password"]}
        for account in yaml.safe_load(TESTING_ACCOUNTS)
        if is_gmail_account(account)
    ]


if __name__ == "__main__":
    print(testing_accounts())
