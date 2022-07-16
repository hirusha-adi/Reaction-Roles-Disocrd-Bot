# Discord Bot for Reaction Roles

simple reaction roles bot discord made with discord.py 

# Installation Guide

## Ubuntu/Debian

1. Install `python3`, `git`, a text editor (`nano`)

    ```bash
    sudo apt install python3 python3-pip git nano
    python3 -m pip install discord
    ```

2. Clone the repository / Download the code and extract and open a console/terminal in that directory 

    ```bash
    git clone "https://github.com/hirusha-adi/Reaction-Roles-Disocrd-Bot.git"
    cd ./Reaction-Roles-Disocrd-Bot
    ```

3. Install dependencies for the bot 

    ```bash
    python3 -m pip install -r requirements.txt
    ```

4. Set the bot token
    ```bash
    nano token.txt
    ```
    1. paste the token (Ctrl+Shift+V)
    2. save the file (Ctrl+S)
    3. exit (Ctrl+X)

5. Edit the `settings.json` to suite your needs

    ```json
    {
        "channel_id": 12345,
        "server_id": 12345,
        "log_channel_id": 12345,
        "message": "text",
        "roles": [
            {
                "name": "text",
                "id": 12345,
                "reaction": "🎥"
            },
            {
                "name": "text2",
                "id": 12345,
                "reaction": "🎵"
            }
        ]
    }
    ```

    <table>
    <thead>
    <tr>
        <th>Key Name</th>
        <th>Data Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>channel_id</td>
        <td>integer</td>
        <td>The discord channel ID to send the text</td>
    </tr>
    <tr>
        <td>server_id</td>
        <td>integer</td>
        <td>The discord server ID to setup</td>
    </tr>
    <tr>
        <td>log_channel_id</td>
        <td>integer</td>
        <td>The discord channel ID to send the log of reaction roles</td>
    </tr>
    <tr>
        <td>log_channel_id</td>
        <td>integer</td>
        <td>The discord channel ID to send the log of reaction roles</td>
    </tr>
    <tr>
        <td>message</td>
        <td>string</td>
        <td>The message to send to channel_id in server_id discord server, the reactions will be added to this message</td>
    </tr>
    <tr>
        <td>roles[x].name</td>
        <td>string</td>
        <td>Name of the discord role</td>
    </tr>
    <tr>
        <td>roles[x].id</td>
        <td>string</td>
        <td>ID of the discord role</td>
    </tr>
    <tr>
        <td>roles[x].reaction</td>
        <td>string</td>
        <td>The emoji to react to for this role to message</td>
    </tr>
    </tbody>
    </table>

    - the `settings.json` is already filled with some sample data, make sure to replce them

6. Start the discord bot

    ```
    python3 bot.py
    ```