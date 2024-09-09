import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="weather", description="Get the current weather for a city")
    async def weather(self, interaction: discord.Interaction, city: str):
        # Use Open-Meteo's free API
        async with aiohttp.ClientSession() as session:
            geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            async with session.get(geocoding_url) as geo_resp:
                if geo_resp.status == 200:
                    geo_data = await geo_resp.json()

                    if not geo_data['results']:
                        await interaction.response.send_message(f"City '{city}' not found.")
                        return

                    # Get the latitude and longitude of the city
                    latitude = geo_data['results'][0]['latitude']
                    longitude = geo_data['results'][0]['longitude']

                    # Now fetch the weather data for that location
                    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
                    async with session.get(weather_url) as weather_resp:
                        if weather_resp.status == 200:
                            weather_data = await weather_resp.json()
                            current_weather = weather_data['current_weather']
                            temperature = current_weather['temperature']
                            windspeed = current_weather['windspeed']
                            description = current_weather['weathercode']  # This is just a numeric code, you'd have to interpret it.

                            await interaction.response.send_message(f"Weather in {city}: {description}, {temperature:.2f}°C, Windspeed: {windspeed} km/h")
                        else:
                            await interaction.response.send_message(f"Could not retrieve weather for {city}")
                else:
                    await interaction.response.send_message(f"Could not find the city '{city}'.")

async def setup(bot):
    await bot.add_cog(Weather(bot))
