# Discloud

A locally run Discord bot that turns your personal Discord server into an unlimited cloud storage service.

## Installation

*   Requires Python 3.x
*   Clone this repo using `git clone https://github.com/4rnv/Discloud.git`
*   Run `pip install -r requirements.txt`

## Usage

1.  Enable Developer mode on Discord.
    - On Discord, head into User Settings > Appearance > Advanced & enable Developer Mode.
2.  Create a basic Discord bot by following the instructions on the Discord Developer Portal.
    - https://discord.com/developers/applications
    - https://discord.com/developers/docs/quick-start/getting-started.
    - Allow it to upload files and send messages.
3.  Add that bot to your server (refer to Guild installation in above links).
4.  Copy your channel ID (right click on channel name) and bot token (from bot page), then add them to the `.env` file in the same directory as `app.py`. Name them as **CHANNEL_ID** and **BOT_TOKEN** respectively.
2.  In the `app.py` file, specify the path to the folder you want to monitor for new files, default is **/upload**.
3.  Run the bot using Python: `python app.py`
## Notes

*   Your bot needs permissions to upload files to the server.
*   `db.json` file stores info about the files which have been uploaded, do not delete it.
*   Error `ModuleNotFoundError: No module named 'audioop'`: Refer to https://github.com/Rapptz/discord.py/issues/9742. This project does not require audioop module, which has been deprecated post Python 3.13. To fix this error, simply comment out `import audioop` from the player.py file in the discord.py package.