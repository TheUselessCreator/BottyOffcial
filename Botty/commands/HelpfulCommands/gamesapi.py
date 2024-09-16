import discord
from discord.ext import commands
import random
import os

class GameAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="gameapi", description="Get a random link from the API")
    async def gameapi(self, ctx):
        # Path to the websiteapi.txt file
        file_path = os.path.join('assets', 'websiteapi.txt')

        # Check if the file exists
        if not os.path.exists(file_path):
            await ctx.send("The API file could not be found.")
            return
        
        # Read the file and get a random link
        with open(file_path, 'r') as f:
            links = [line.strip() for line in f if line.strip()]
        
        # Ensure there are links to choose from
        if not links:
            await ctx.send("No links are available in the API file.")
            return
        
        # Select a random link
        random_link = random.choice(links)
        
        # Send the random link as a response
        await ctx.send(f"Here is your random link: {random_link}")

# Function to setup the cog
def setup(bot):
    bot.add_cog(GameAPI(bot))
