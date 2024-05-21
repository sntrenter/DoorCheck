import discord
from discord.ext import commands
from TOKEN import TOKEN
import os
intents = discord.Intents.default()  # Create a default intents object

# Add the specific intents your bot needs
intents.message_content = True  # Allows reading message content
#intents.message_reactions = True  # Allows reacting to messages


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # Check if the message is from the bot itself to avoid reacting to its own messages.
    if message.author == bot.user:
        return

    # Check if the message was sent in the target channel
    target_channel = discord.utils.get(message.guild.channels, name="garagedoor")
    if message.channel == target_channel:
        # React to the message with a thumbs-up emoji.
        thumbs_up_emoji = '\U0001F44D'  # Unicode for the thumbs-up emoji
        await message.add_reaction(thumbs_up_emoji)

        if os.path.exists("door.jpg"):
            os.remove("door.jpg")
        
        os.system("raspistill -t 1 -ex auto -br 80 -co 95 -ISO 800 -ev 5 -o door.jpg")

        if os.path.exists("door.jpg"):
            with open("door.jpg", "rb") as f:
                image = discord.File(f)
                await message.channel.send(file=image)
        else:
            await message.channel.send("Error: Couldn't capture the image.")

bot.run(TOKEN)
