
import discord
from discord.ext import commands
import os
import importlib
from dotenv import load_dotenv
import tracemalloc
import asyncio

# Load environment variables from the .env file
load_dotenv()

# Initialize tracemalloc to track memory allocation
tracemalloc.start()

# Get the bot token and application ID from environment variables
TOKEN = os.getenv('TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')

if not TOKEN:
    raise ValueError("Error: TOKEN environment variable not set. Please check your .env file.")

if not APPLICATION_ID:
    raise ValueError("Error: APPLICATION_ID environment variable not set. Please check your .env file.")

# Set up Discord intents (including message content)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # Needed for syncing slash commands
intents.members = True  # Make sure member intent is enabled for roles and user management

# Create the bot instance with command prefix, intents, and application_id
bot = commands.Bot(command_prefix='/', intents=intents, application_id=APPLICATION_ID)

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

    # Sync slash commands globally
    try:
        await bot.tree.sync()
        print("Slash commands synced successfully!")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

# Load commands from a given folder recursively
async def load_commands_from_folder(folder_name):
    commands_path = os.path.join(os.path.dirname(__file__), folder_name)
    if not os.path.isdir(commands_path):
        print(f"{folder_name} directory not found: {commands_path}")
        return

    for root, dirs, files in os.walk(commands_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                # Construct the module name from the file path
                relative_path = os.path.relpath(root, commands_path)
                if relative_path == '.':
                    module_name = f'{folder_name}.{file[:-3]}'
                else:
                    module_name = f'{folder_name}.{relative_path.replace(os.path.sep, ".")}.{file[:-3]}'
                
                try:
                    # Dynamically import the module
                    importlib.import_module(module_name)
                    await bot.load_extension(module_name)
                    print(f'Loaded {file} successfully from {folder_name}.')
                except Exception as e:
                    print(f'Failed to load {file} from {folder_name}: {e}')

# Load commands from the commands and PrefixCommands folders
async def load_commands():
    await load_commands_from_folder('commands')
    await load_commands_from_folder('PrefixCommands')

# Run the bot
async def start_bot():
    # Load commands from the commands folders
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
