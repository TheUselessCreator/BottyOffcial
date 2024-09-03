import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
import datetime

# Load the .env file
load_dotenv()

class ServerJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Send a webhook message when the bot joins a new server."""
        # Get the webhook URL from the .env file
        webhook_url = os.getenv("JOIN_WEBHOOK")

        if webhook_url is None:
            print("Webhook URL is not set. Please check the .env file.")
            return

        # Get guild (server) information
        server_name = guild.name
        server_id = guild.id
        owner = guild.owner
        owner_name = owner.name
        owner_id = owner.id
        creation_date = guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
        member_count = guild.member_count
        icon_url = guild.icon.url if guild.icon else "No icon"

        # Create the payload for the webhook
        data = {
            "username": "Botty Notification",
            "embeds": [
                {
                    "title": f"Botty joined a new server!",
                    "color": 0x00ff00,
                    "fields": [
                        {"name": "Server Name", "value": server_name, "inline": True},
                        {"name": "Server ID", "value": str(server_id), "inline": True},
                        {"name": "Owner", "value": f"{owner_name} (ID: {owner_id})", "inline": True},
                        {"name": "Creation Date", "value": creation_date, "inline": True},
                        {"name": "Member Count", "value": str(member_count), "inline": True}
                    ],
                    "thumbnail": {"url": icon_url}
                }
            ]
        }

        # Send the POST request to the webhook URL
        response = requests.post(webhook_url, json=data)

        # Log any potential errors
        if response.status_code != 204:
            print(f"Error sending webhook: {response.status_code}, {response.text}")

# Set up the cog
async def setup(bot):
    await bot.add_cog(ServerJoin(bot))
