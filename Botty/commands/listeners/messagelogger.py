import discord
from discord.ext import commands
import logging
import os
from datetime import datetime

class MessageLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Set up logging
        log_dir = 'assets'
        log_file = os.path.join(log_dir, 'logger.txt')

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)  # Create the 'assets' directory if it doesn't exist

        # Configure the logging to write to 'logger.txt'
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Logs all messages to logger.txt"""
        if message.author.bot:
            return

        # Log message in the specified format
        log_message = f"User: {message.author} (ID: {message.author.id}) | Channel: {message.channel.name} (ID: {message.channel.id}) | Message: {message.content}"
        logging.info(log_message)

async def setup(bot):
    await bot.add_cog(MessageLogger(bot))
