import discord
from discord.ext import commands
import os

class InviteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="invite", description="Get the bot's invite link")
    async def invite(self, interaction: discord.Interaction):
        client_id = os.getenv("CLIENT_ID")
        if client_id:
            invite_link = f"https://discord.com/oauth2/authorize?client_id={client_id}&scope=bot&permissions=8"
            await interaction.response.send_message(f"Invite me to your server using this link: {invite_link}")
        else:
            await interaction.response.send_message("Client ID is not set.")

async def setup(bot):
    await bot.add_cog(InviteCommand(bot))
