import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import tracemalloc
import asyncio

# Load environment variables from the .env file
load_dotenv()

# Initialize tracemalloc to track memory allocation
tracemalloc.start()

# Get the bot token from environment variables
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    raise ValueError("Error: TOKEN environment variable not set. Please check your .env file.")

# Set up Discord intents (including message content)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # Needed for syncing slash commands

# Create the bot instance with command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Function to set the bot's status from status.txt
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

    # Set status from the status.txt file
    await set_status()

    # Sync slash commands
    try:
        await bot.tree.sync()
        print("Slash commands synced successfully!")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

# Load commands from the commands folder
async def load_commands():
    commands_path = os.path.join(os.path.dirname(__file__), 'commands')
    if not os.path.isdir(commands_path):
        print(f"Commands directory not found: {commands_path}")
        return

    for filename in os.listdir(commands_path):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f'Loaded {filename} successfully.')
            except Exception as e:
                print(f'Failed to load {filename}: {e}')

# Run the bot
async def start_bot():
    # Load commands from the commands folder
    await load_commands()

    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f"An error occurred while running the bot: {e}")
        # Capture and display memory allocations on error
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        print("Memory allocation snapshot at error:")
        for index, stat in enumerate(top_stats[:10], start=1):
            print(f"#{index}: {stat}")

# Run the bot
if __name__ == "__main__":
    asyncio.run(start_bot())