# Table of Contents
- [Table of Contents](#table-of-contents)
- [Terminology](#terminology)
- [Usage](#usage)
- [Getting a Token](#getting-a-token)
- [Get room info](#get-room-info)
- [Troubleshooting - More cURL](#troubleshooting---more-curl)

# Terminology
- Channel: public chat area
- Group: private chat area
- Room: generic term for both of the above items

# Usage

Collect the following data and place in the `config.ini` config file
- generate a token
- gather data needed and place in config file
  - token
  - userid for token (this is generated at the same time as the token, and is NOT your login user ID)
  - the URI of your rocketchat server (the fully qualified domain name of the server, most likely)
  - room you want to get users for

After valid data is in the config file, simply run the `statuser.py` script. It will create a `.csv` file named according to the following pattern: `status_YYYYMMDD.csv`. Multiple runs on the same day overwrite the output file.

# Getting a Token

This only needs to be done on the initial run.

Generate a token following the directions here:  
https://rocket.chat/docs/developer-guides/rest-api/personal-access-tokens/


# Get room info

This should only need to be done the first time the config file is set up.

This command lists all groups a user is part of and prints out a list of room names in the correct format to use in the config file.

```bash
curl -k -H "X-Auth-Token: myauthtoken" \
    -H "X-User-Id: myuserid" \
    https://yourrocketchatserver.org/api/v1/groups.list | \
    jq -r '.groups[] | .name'
```


# Troubleshooting - More cURL

List info about rocketchat instance - good for validating a token, also works without auth

```bash
curl -k -H "X-Auth-Token: myauthtoken" \
    -H "X-User-Id: myuserid" \
    https://yourrocketchatserver.org/api/v1/info
```

This command is basically a simpler

Status is going to be things like "away", "offline", "online". StatusText will be the user defined detailed status such as "Telework" or "In the bathroom".

```bash
curl -k -H "X-Auth-Token: myauthtoken" \
    -H "X-User-Id: myuserid" \
    https://yourrocketchatserver.org/api/v1/groups.members?roomName=yourRoomName | \
jq -r '.members[] | [.name, .status, .statusText] | @csv'
```
