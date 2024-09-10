import discord
from discord import app_commands
from discord.ext import commands

class PicrossCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="picross", description="Fill in a 5x5 grid based on a number code.")
    async def picross(self, interaction: discord.Interaction, numbercode: str):
        # Validate the number code length
        if len(numbercode) != 25 or not numbercode.isdigit():
            await interaction.response.send_message("Please provide a valid 25-digit number code.")
            return

        # Create a 5x5 grid
        grid = [[' ' for _ in range(5)] for _ in range(5)]

        # Fill in the grid based on the number code
        for i in range(5):
            for j in range(5):
                if numbercode[i * 5 + j] == '1':
                    grid[i][j] = '🟦'  # Blue Square for filled
                else:
                    grid[i][j] = '⬜'  # White Square for empty

        # Format the grid into a string
        grid_string = '\n'.join(' '.join(row) for row in grid)
        
        # Send the grid as a response
        await interaction.response.send_message(f"```\n{grid_string}\n```")

async def setup(bot: commands.Bot):
    await bot.add_cog(PicrossCommand(bot))
