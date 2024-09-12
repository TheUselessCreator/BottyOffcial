import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the user ID from the environment variables
USER_ID = int(os.getenv('USER_ID'))

class MessageLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='getmessagelogger', description="Get the message logs from the bot")
    async def get_message_logger(self, ctx):
        """Allows the specified USER_ID from the .env file to retrieve the message log file"""
        # Check if the user issuing the command is the authorized user
        if ctx.author.id != USER_ID:
            await ctx.send("You don't have permission to use this command.")
            return
        
        log_file_path = os.path.join('assets', 'logger.txt')

        # Check if the log file exists
        if os.path.exists(log_file_path):
            # Send the log file to the user
            await ctx.send(file=discord.File(log_file_path, 'logger.txt'))
        else:
            await ctx.send("No log file found!")

async def setup(bot):
    await bot.add_cog(MessageLogger(bot))
