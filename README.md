# Drivemode QA Satellite

## About
The purpose of this tool is to maintain testing accounts active by sending automated emails in accordance with Google's Inactivity Policy.
<br><br>
<a href="https://support.google.com/accounts/answer/12418290?hl=en" target="_blank">Inactive Google Account Policy</a>

## Setup Bitwarden CLI
1. <a href="https://bitwarden.com/help/cli/" target="_blank">Download and install the Bitwarden CLI</a>
2. <a href="https://bitwarden.com/help/personal-api-key/" target="_blank">Get your personal API Key</a>
3. Use your personal API key to log in to the Bitwarden CLI, then enter your unique client_id and client_secret. To log in with the API Key:
```commandline
bw login --apikey
bw unlock
```

## Usage
1. In `./artifacts/predefined.yaml`, enter the predefined values:
```yaml
bad_accounts:
  - badaccount1@gmail.com
  - badaccount2@gmail.com

default_recipient: default_recipient@gmail.com
collection_id: bitwarden-collections-id
```
<b>bad_accounts</b> <i>(list) [Optional]</i>:
Accounts that cannot be authenticated or have incorrect passwords.

<b>default_recipient</b> <i>(str)</i>:
If the tool is unable to generate an email recipient, this is the default one.

<b>collection_id</b> <i>(str)</i>:
The bitwarden collection ID that needs to be activated, such the Testing Accounts collection.

2. Start the program:
```commandline
./quickstart
```
3. When prompted, enter your Bitwarden Master Password.

## Improvements
1. Implement `next` or error handling when a Google account has a problem, such as an incorrect password or a failure to authenticate.
2. Implement Login and OAuth 2.0 using API keys to achieve full automation. Currently, login and authorization are done manually.
3. Conceal the `client_secret`. Since it is an internal tool, even if it is currently exposed, the risk is very low.
