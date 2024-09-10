import discord
from discord.ext import commands
from discord import app_commands
import os

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.autorespond_enabled = True  # Default state is enabled
        self.responses = self.load_responses()  # Load responses from the file

    def load_responses(self):
        """Load autoresponses from words.txt."""
        responses = {}
        # Construct the path to words.txt, assuming it's in Botty/autoresponderfolder
        base_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        # Assuming that 'autoresponderfolder' is a sibling directory to the current script's directory
        folder_path = os.path.join(base_path, '..', 'autoresponderfolder', 'words.txt')
        folder_path = os.path.abspath(folder_path)  # Convert to absolute path

        print(f"Looking for words.txt at: {folder_path}")

        try:
            with open(folder_path, 'r') as file:
                for line in file.readlines():
                    if '=' in line:
                        key, response = line.strip().split('=', 1)
                        responses[key.lower()] = response
        except FileNotFoundError:
            print(f"words.txt file not found at {folder_path}")
        except Exception as e:
            print(f"An error occurred while loading responses: {e}")
        return responses

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Respond to messages if autoresponder is enabled."""
        if message.author.bot:
            return  # Ignore bot messages
        if not self.autorespond_enabled:
            return  # If autoresponder is disabled, don't respond

        for word, response in self.responses.items():
            if word.lower() in message.content.lower():
                await message.channel.send(response)
                break

    @app_commands.command(name="autorespondenable", description="Enable the autoresponder")
    async def autorespondenable(self, interaction: discord.Interaction):
        """Enable the autoresponder."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        self.autorespond_enabled = True
        await interaction.response.send_message("Autoresponder has been enabled.", ephemeral=True)

    @app_commands.command(name="autoresponddisable", description="Disable the autoresponder")
    async def autoresponddisable(self, interaction: discord.Interaction):
        """Disable the autoresponder."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        self.autorespond_enabled = False
        await interaction.response.send_message("Autoresponder has been disabled.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoResponder(bot))
