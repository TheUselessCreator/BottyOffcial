import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import asyncio
import importlib
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the bot token and application ID from environment variables
TOKEN = os.getenv('TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')

if not TOKEN:
    raise ValueError("Error: TOKEN environment variable not set. Please check your .env file.")

if not APPLICATION_ID:
    raise ValueError("Error: APPLICATION_ID environment variable not set. Please check your .env file.")

# Load prefixes from JSON file
def load_prefixes():
    if os.path.exists('prefixes.json'):
        with open('prefixes.json', 'r') as f:
            return json.load(f)
    else:
        return {}

# Save prefixes to JSON file
def save_prefixes(prefixes):
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

# Function to dynamically get the prefix for each guild
async def get_prefix(bot, message):
    prefixes = load_prefixes()  # Always load the latest prefixes from the file
    guild_id = str(message.guild.id)
    return prefixes.get(guild_id, "/")  # Default to "/" if no custom prefix is set

# Initialize bot with dynamic prefix getter
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents, application_id=APPLICATION_ID)

# Slash command to set the prefix for the current server
@bot.tree.command(name="setprefix", description="Set a custom prefix for this server.")
async def set_prefix(interaction: discord.Interaction, prefix: str):
    """Set a custom prefix for the server using a slash command."""
    guild_id = str(interaction.guild.id)
    prefixes = load_prefixes()  # Load the current prefixes
    prefixes[guild_id] = prefix  # Update the prefix for this guild
    save_prefixes(prefixes)  # Save the updated prefixes to the file
    await interaction.response.send_message(f"Prefix set to `{prefix}` for this server.")

# Function to load commands from the commands folder
async def load_commands():
    commands_path = os.path.join(os.path.dirname(__file__), 'commands')
    if not os.path.isdir(commands_path):
        print(f"Commands directory not found: {commands_path}")
        return

    for root, dirs, files in os.walk(commands_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                # Construct the module name from the file path
                relative_path = os.path.relpath(root, commands_path)
                if relative_path == '.':
                    module_name = f'commands.{file[:-3]}'
                else:
                    module_name = f'commands.{relative_path.replace(os.path.sep, ".")}.{file[:-3]}'

                try:
                    # Dynamically import the module
                    importlib.import_module(module_name)
                    await bot.load_extension(module_name)
                    print(f'Loaded {file} successfully.')
                except Exception as e:
                    print(f'Failed to load {file}: {e}')

# Event for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    # Sync slash commands globally
    try:
        await bot.tree.sync()
        print("Slash commands synced successfully!")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

# Run the bot
async def start_bot():
    # Load commands from the commands folder
    await load_commands()

    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f"An error occurred while running the bot: {e}")

# Run the bot
if __name__ == "__main__":
    asyncio.run(start_bot())
