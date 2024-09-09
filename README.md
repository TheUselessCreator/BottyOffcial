# Botty 🤖
Botty is a customizable Discord bot built using Python and the discord.py library. This bot comes packed with a variety of features including anti-spam measures, emoji limits, and customizable commands to enhance your Discord server experience.

# Features
Anti-Spam Detection: Automatically timeout users who exceed a certain number of messages in a time window.
Emoji Limit: Limit the number of emojis users can send in a message, and automatically delete messages that exceed the limit.
Custom Commands: Easily add custom commands to fit the needs of your server.
Admin Commands: Enable or disable specific features such as anti-spam and emoji limits.
Role Management: Manage roles and permissions with admin-only commands.
Requirements
Python 3.8+
discord.py 2.0+
asyncio
# Installation
Clone the repository:
bash
Copy code
git clone https://github.com/TheUselessCreator/BottyOffcial
cd botty
# Install dependencies:
bash
Copy code
pip install -r requirements.txt
Set up your bot token:
Create a .env file in the project root and add your bot token like so:

# makefile
Copy code
DISCORD_TOKEN=your-discord-bot-token
# Run the bot:
bash
Copy code
python botty.py
# Commands
Admin Commands
/antispamenable: Enable anti-spam for the server.
/antispamdisable: Disable anti-spam for the server.
/emojilimitenable (amount): Enable an emoji limit for the server.
/emojilimitdisable: Disable the emoji limit.
/kick (user): Kick a user from the server.
/ban (user): Ban a user from the server.
Utility Commands
/say (message) (channel): Make the bot send a message to the specified channel.
/deletemessages (amount) (channel): Bulk delete messages from a channel.
# Contributing
Contributions are welcome! Feel free to submit issues or pull requests. Make sure to fork the repository and work on a new branch before submitting any pull requests.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Contact
If you have any questions or issues, please contact me via Discord: theuselesscreator_offical or open an issue on GitHub.
