import os
import re
from typing import List

import yaml

with open("artifacts/predefined.yaml", "r") as yml:
    predefined = yaml.safe_load(yml)


def is_valid_account(account: dict) -> bool:
    try:
        return (
            re.search(r"Google", account["name"])
            and account["login"]["username"] not in predefined["bad_accounts"]
        )
    except KeyError:
        return False


def testing_accounts() -> List:
    """Fetch testing accounts from Bitwarden.
    Returns:
        Valid Testing Accounts.
    """
    collection_id = predefined["collection_id"]
    test_accounts = os.popen(f"bw list items --collectionid {collection_id}").read()
    tf = lambda x: x + "@gmail.com" if not x.endswith("@gmail.com") else x
    return [
        tf(acc["login"]["username"])
        for acc in yaml.safe_load(test_accounts)
        if is_valid_account(acc)
    ]


def email_to() -> str:
    return predefined["default_recipient"]


if __name__ == "__main__":
    print(testing_accounts())
