import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the webhook URL from the .env file
WEBHOOK_URL = os.getenv('JOIN_WEBHOOK_URL')

class ServerJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if WEBHOOK_URL is None:
            print("Webhook URL is not set in the .env file!")
            return

        # Information about the server
        server_id = guild.id
        server_name = guild.name
        member_count = guild.member_count
        owner = guild.owner

        # Webhook message content
        data = {
            "content": None,
            "embeds": [
                {
                    "title": "Server joined!",
                    "description": f"**Server ID**: {server_id}\n"
                                   f"**Server Name**: {server_name}\n"
                                   f"**Member Count**: {member_count}\n"
                                   f"**Owner**: {owner}",
                    "color": 3066993  # Optional: Embed color
                }
            ],
            "username": "Server Join Bot"  # Webhook bot name
        }

        # Send the POST request to the webhook URL
        response = requests.post(WEBHOOK_URL, json=data)

        # Check for any errors
        if response.status_code != 204:
            print(f"Error sending webhook: {response.status_code} - {response.text}")

async def setup(bot):
    await bot.add_cog(ServerJoin(bot))
