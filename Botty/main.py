import discord
from discord.ext import commands
import json
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load prefixes from JSON file
def load_prefixes():
    if os.path.exists('prefixes.json'):
        with open('prefixes.json', 'r') as f:
            return json.load(f)
    else:
        return {}

# Function to dynamically get the prefix for each guild
async def get_prefix(bot, message):
    prefixes = load_prefixes()
    guild_id = str(message.guild.id)
    return prefixes.get(guild_id, "/")  # Default to "/" if no custom prefix is set

# Initialize bot with dynamic prefix getter
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=get_prefix, intents=intents)

# Function to set the bot's status
async def set_status():
    try:
        status_path = os.path.join(os.path.dirname(__file__), 'assets', 'status.txt')
        with open(status_path, 'r') as file:
            status_text = file.read().strip()
            if not status_text:
                status_text = "Default status"  # Fallback status text
            await bot.change_presence(activity=discord.Game(name=status_text), status=discord.Status.online)
            print(f"Status set to: {status_text}")
    except Exception as e:
        print(f"Failed to set status: {e}")

# Event for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await set_status()
    try:
        await bot.tree.sync()
        print("Slash commands synced successfully!")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

# Setup function to load cogs from the commands folder
async def load_cogs():
    commands_path = os.path.join(os.path.dirname(__file__), 'commands')
    for root, _, files in os.walk(commands_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                relative_path = os.path.relpath(root, commands_path)
                if relative_path == '.':
                    module_name = f'commands.{file[:-3]}'
                else:
                    module_name = f'commands.{relative_path.replace(os.path.sep, ".")}.{file[:-3]}'
                try:
                    await bot.load_extension(module_name)
                    print(f'Loaded {file} successfully.')
                except Exception as e:
                    print(f'Failed to load {file}: {e}')

# Run the bot
async def main():
    await load_cogs()
    try:
        await bot.start(os.getenv('TOKEN'))
    except Exception as e:
        print(f"An error occurred while running the bot: {e}")

# Start the bot
if __name__ == "__main__":
    asyncio.run(main())
