import discord
from discord.ext import commands
import os

# Load the user ID from the .env file
from dotenv import load_dotenv
load_dotenv()
USER_ID = int(os.getenv('USER_ID'))  # Ensure USER_ID is defined in your .env file

class MessageLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='getmessagelogger', help='Send the log file to the owner.')
    async def get_message_logger(self, ctx):
        if ctx.author.id == USER_ID:
            # Define the path to the log file
            log_file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logger.txt')

            # Check if the log file exists
            if os.path.exists(log_file_path):
                # Send the log file
                await ctx.author.send(file=discord.File(log_file_path))
                await ctx.send("Log file sent to your DMs.")
            else:
                await ctx.send("Log file not found.")
        else:
            await ctx.send("You do not have permission to use this command.")

async def setup(bot):
    # Before loading the cog, check if it's already loaded and unload if necessary
    if bot.get_cog('MessageLogger') is not None:
        await bot.unload_extension('commands.OwnerCommands.OwnerMSGget')
    
    # Now load the cog
    await bot.add_cog(MessageLogger(bot))

