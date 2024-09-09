import discord
from discord.ext import commands
import aiohttp
import os
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
JOIN_WEBHOOK = os.getenv('JOIN_WEBHOOK')

class ServerJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Send a webhook message when the bot joins a new server."""
        if not JOIN_WEBHOOK:
            print("JOIN_WEBHOOK not set. Please check your .env file.")
            return

        # Guild (server) information
        server_name = guild.name
        server_id = guild.id
        owner = guild.owner
        owner_name = owner.name
        owner_id = owner.id
        creation_date = guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
        member_count = guild.member_count
        icon_url = guild.icon.url if guild.icon else "No icon"

        # Current timestamp
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create embed for webhook
        embed = discord.Embed(
            title=f"Botty joined a new server!",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Server Name", value=server_name, inline=True)
        embed.add_field(name="Server ID", value=str(server_id), inline=True)
        embed.add_field(name="Owner", value=f"{owner_name} (ID: {owner_id})", inline=True)
        embed.add_field(name="Creation Date", value=creation_date, inline=True)
        embed.add_field(name="Member Count", value=str(member_count), inline=True)
        embed.add_field(name="Joined At", value=current_time, inline=True)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        # Send POST request to webhook
        async with aiohttp.ClientSession() as session:
            webhook_data = {"embeds": [embed.to_dict()]}
            async with session.post(JOIN_WEBHOOK, json=webhook_data) as response:
                if response.status == 204:
                    print(f"Successfully sent webhook for joining {server_name}")
                else:
                    print(f"Failed to send webhook: {response.status} - {await response.text()}")

# Add the cog to the bot
async def setup(bot: commands.Bot):
    await bot.add_cog(ServerJoin(bot))
