import os
import re
from typing import List

import yaml


def is_gmail_account(account: dict) -> bool:
    try:
        if re.search(r"Google", account["name"]):
            return True
    except KeyError:
        return False


def get_testing_accounts() -> List:
    with open("artifacts/predefined.yaml", "r") as yml:
        collection_id = yaml.safe_load(yml)["collection_id"]
    test_accounts = os.popen(f"bw list items --collectionid {collection_id}").read()
    return [
        acc["login"]["username"]
        for acc in yaml.safe_load(test_accounts)
        if is_gmail_account(acc)
    ]


if __name__ == "__main__":
    print(get_testing_accounts())
