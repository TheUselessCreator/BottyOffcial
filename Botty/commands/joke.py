import discord
from discord.ext import commands
from discord import app_commands
import requests

class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="joke", description="Get a random joke.")
    async def joke(self, interaction: discord.Interaction):
        # JokeAPI URL for a random joke
        url = "https://v2.jokeapi.dev/joke/Any"

        # Fetch joke data from JokeAPI
        response = requests.get(url)

        if response.status_code != 200:
            await interaction.response.send_message("Failed to retrieve joke.", ephemeral=True)
            return

        # Parse the JSON response
        json_response = response.json()

        if json_response.get("type") == "single":
            joke = json_response.get("joke")
        elif json_response.get("type") == "twopart":
            setup = json_response.get("setup")
            delivery = json_response.get("delivery")
            joke = f"{setup} - {delivery}"
        else:
            joke = "No joke found."

        # Send the joke as a message
        await interaction.response.send_message(joke)

async def setup(bot):
    await bot.add_cog(Joke(bot))
