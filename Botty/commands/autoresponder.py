import discord
from discord.ext import commands
import os

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = {}
        self.load_responses()
        self.load_status()

    def load_responses(self):
        """Load responses from words.txt."""
        try:
            words_path = os.path.join(os.path.dirname(__file__), '..', 'autoresponderfolder', 'words.txt')
            with open(words_path, 'r') as file:
                for line in file:
                    if '=' in line:
                        trigger, response = line.strip().split('=', 1)
                        self.responses[trigger.lower()] = response
        except Exception as e:
            print(f"Failed to load responses: {e}")

    def load_status(self):
        """Load auto-responder status from enabled.txt."""
        try:
            status_path = os.path.join(os.path.dirname(__file__), '..', 'autoresponderfolder', 'enabled.txt')
            with open(status_path, 'r') as file:
                status = file.read().strip().lower()
                self.enabled = status == 'enabled'
        except Exception as e:
            print(f"Failed to load status: {e}")
            self.enabled = False

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Respond to messages based on the loaded responses."""
        if not self.enabled:
            return
        
        if message.author == self.bot.user:
            return  # Ignore messages from the bot itself

        content = message.content.lower()
        for trigger, response in self.responses.items():
            if trigger in content:
                await message.channel.send(response)
                break

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoResponder(bot))
