# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord

# IMPORT THE OS MODULE.
import os

# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv


# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client()


# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".

	message_text = message.content.lower()
	
	if message_text.find("hello") != -1:
		# SENDS BACK A MESSAGE TO THE CHANNEL.
		await message.channel.send("Hello jedi! May the force be with you!")
		return
	elif message_text.find("bonjour") != -1:
		# SENDS BACK A MESSAGE TO THE CHANNEL.
		await message.channel.send("Bonjour jedi! Que le force soit avec toi!")
		return
	elif message_text.find("grogu") != -1:
		# SENDS BACK A MESSAGE TO THE CHANNEL.
		await message.channel.send("Where's Mando?")
		return
	elif message_text.find("mando") != -1:
		# SENDS BACK A MESSAGE TO THE CHANNEL.
		await message.channel.send("This is the way!")
		return





# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)