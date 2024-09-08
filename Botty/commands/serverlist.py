import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import math
import os
from dotenv import load_dotenv

# Load the USER_ID from the .env file
load_dotenv()
AUTHORIZED_USER_ID = int(os.getenv('USER_ID'))

class ServerPaginator(discord.ui.View):
    def __init__(self, servers, per_page=10):
        super().__init__()
        self.servers = servers
        self.per_page = per_page
        self.current_page = 0
        self.max_page = math.ceil(len(servers) / per_page) - 1

        # Disable Prev button initially if we're on the first page
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.max_page

    def get_page(self):
        """Get the servers for the current page."""
        start = self.current_page * self.per_page
        end = start + self.per_page
        return self.servers[start:end]

    async def update_embed(self, interaction: discord.Interaction):
        """Update the embed message to reflect the current page."""
        embed = discord.Embed(
            title=f"Servers (Page {self.current_page + 1}/{self.max_page + 1})",
            description="\n".join(
                [f"{i + 1}. {server.name} (ID: {server.id})" for i, server in enumerate(self.get_page())]
            ),
            color=discord.Color.blue()
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Prev', style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.max_page
        await self.update_embed(interaction)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.max_page
        await self.update_embed(interaction)

class ServerList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="servers", description="List servers the bot is in (only for authorized users)")
    async def servers(self, interaction: discord.Interaction):
        """Show a paginated list of servers the bot is in."""
        if interaction.user.id != AUTHORIZED_USER_ID:
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return
        
        # Get the list of servers the bot is in
        servers = self.bot.guilds

        if not servers:
            await interaction.response.send_message("The bot is not in any servers.", ephemeral=True)
            return

        # Create a paginated view for servers
        paginator = ServerPaginator(servers)
        embed = discord.Embed(
            title="Servers (Page 1)",
            description="\n".join(
                [f"{i + 1}. {server.name} (ID: {server.id})" for i, server in enumerate(paginator.get_page())]
            ),
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, view=paginator)

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerList(bot))
