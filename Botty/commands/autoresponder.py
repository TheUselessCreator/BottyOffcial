import discord
from discord.ext import commands

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = {}

        # Load the responses from the words.txt file
        self.load_responses()

    def load_responses(self):
        try:
            with open('./autoresponderessentials/words.txt', 'r') as file:
                lines = file.readlines()
                print("File contents:")
                for line in lines:
                    print(f"Read line: {line.strip()}")

                for line in lines:
                    line = line.strip()
                    if line and '=' in line:
                        try:
                            trigger, response = line.split('=', 1)
                            self.responses[trigger.strip().lower()] = response.strip()
                            print(f"Loaded response: trigger='{trigger.strip()}', response='{response.strip()}'")
                        except ValueError:
                            print(f"Skipping improperly formatted line: {line}")

                print(f"Loaded {len(self.responses)} responses.")
        except FileNotFoundError:
            print("words.txt file not found. Please make sure it exists.")
        except Exception as e:
            print(f"An error occurred while loading responses: {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or not message.content.strip():
            return  # Ignore empty messages and messages from the bot itself

        # Check for triggers in the message
        message_content = message.content.lower().strip()
        for trigger, response in self.responses.items():
            if trigger in message_content:
                await message.channel.send(response)
                break

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoResponder(bot))
