import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from dotenv import load_dotenv
import os 

# Load bot server credentials from the env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TESTING_GUILD_ID = int(os.getenv("TESTING_GUILD_ID"))
# bot = commands.Bot(command_prefix="$")

intents = nextcord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(intents = intents)

@bot.slash_command(guild_ids=[TESTING_GUILD_ID], description="Help menu")
async def help(interaction: Interaction):
    await interaction.response.send_message("\nType /ping to get a surprise message. \nType /echo to repeat your message. \nType /enter_a_number to repeat a number. ")


# command will be global if guild_ids is not specified
@bot.slash_command(guild_ids=[TESTING_GUILD_ID], description="Ping command")
async def ping(interaction: Interaction):
    await interaction.response.send_message("Pong!")


@bot.slash_command(guild_ids=[TESTING_GUILD_ID], description="Repeats your message")
async def echo(interaction: Interaction, arg: str = SlashOption(description="Message")):
    await interaction.response.send_message(arg)


@bot.slash_command(guild_ids=[TESTING_GUILD_ID], description="Choose a number")
async def enter_a_number(
    interaction: Interaction,
    number: int = SlashOption(description="Your number", required=False),
):
    if not number:
        await interaction.response.send_message("No number was specified!", ephemeral=True)
    else:
        await interaction.response.send_message(f"You chose {number}!")

# Message Event 
@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')


bot.run(DISCORD_TOKEN)
