import discord
from discord.ext import commands
import random
import os

class GameAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="gameapi", description="Get a random link from the API")
    async def gameapi(self, interaction: discord.Interaction):
        # Path to the websiteapi.txt file
        file_path = os.path.join('assets', 'websiteapi.txt')

        # Check if the file exists
        if not os.path.exists(file_path):
            await interaction.response.send_message("The API file could not be found.")
            return
        
        # Read the file and get a random link
        with open(file_path, 'r') as f:
            links = [line.strip() for line in f if line.strip()]
        
        # Ensure there are links to choose from
        if not links:
            await interaction.response.send_message("No links are available in the API file.")
            return
        
        # Select a random link
        random_link = random.choice(links)
        
        # Send the random link as a response
        await interaction.response.send_message(f"Here is your random link: {random_link}")

# Function to setup the cog
async def setup(bot):
    await bot.add_cog(GameAPI(bot))
