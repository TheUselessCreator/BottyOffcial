import discord
from discord.ext import commands

class GitHubCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="github", description="Get the GitHub repository link")
    async def github(self, interaction: discord.Interaction):
        github_link = "https://github.com/TheUselessCreator/Botty/tree/main"  # Replace with your GitHub link
        await interaction.response.send_message(f"Check out the source code here: {github_link}")

async def setup(bot):
    await bot.add_cog(GitHubCommand(bot))
