# Import the command handler
from nturl2path import url2pathname
import lightbulb
import os
import random
from dotenv import load_dotenv
import hikari
import logging
import requests
import json


def handle_slash_commands(bot):

    jokes = [
        "Why did the programmer leave the camping trip early?\n🥁 Because there were too many bugs! 🐛 🐛 🐛",
        "What did the hacker's out of office message say?\n🥁 Gone phishing. 🎣 🎣 🎣",
        "What do you call a turtle that surfs the Dark Web?\n🥁 A TORtoise. 🧅 🐢 🧅 🐢 🧅 🐢 ",
        "What's a hacker's favourite season?\n🥁 Phishing season. 🎣 🎣 🎣 ",
        "What’s the best way to catch a runaway robot?\n🥁 Use a botnet. 🤖 🥅 ",
        "An SQL statement walks into a bar and sees two tables. It approaches and asks…\n🥁 May I join you? 🍸 🍸 🍸"
    ]

    # Help menu slash command
    @bot.command
    @lightbulb.command("help", "help menu")
    @lightbulb.implements(lightbulb.SlashCommand)
    async def ping(ctx: lightbulb.Context) -> None:
        await ctx.respond("\n/help display help menu. \n/joke tell you a joke. \n/rainfall to get rain fall for the requested long. and lat.\n/verify credibility of the domain by getting the alexa ranking.")

    # Joke slash command
    @bot.command
    @lightbulb.command("joke", "ask for a joke")
    @lightbulb.implements(lightbulb.SlashCommand)
    async def ping(ctx: lightbulb.Context) -> None:
        random_num = random.randrange(0, len(jokes)-1)
        await ctx.respond(jokes[random_num])

    # Verify credibility of URL 
    @bot.command
    @lightbulb.option("url", "url you want to verify", str)
    @lightbulb.command("verify", "verify the alexa ranking of the domain")
    @lightbulb.implements(lightbulb.SlashCommand)
    async def verify(ctx: lightbulb.Context) -> None:
        url= ctx.options.url
        alexa_rank = verify_url(url)
        await ctx.respond("The alexa rank for the "+url+" domain is: "+str(alexa_rank)+ "\nKeep in mind, the lower the alexa ranking, the more popular and credible.")


    # Retrieve the average rain fall for the next 7 days
    @bot.command
    @lightbulb.option("latitude", "latitude", str)
    @lightbulb.option("longitude", "longitude", str)
    @lightbulb.command("rainfall", "retrieve rainfall summary ")
    @lightbulb.implements(lightbulb.SlashCommand)
    async def rainfall(ctx: lightbulb.Context) -> None:
        latitude= ctx.options.latitude
        longitude = ctx.options.longitude
        rainfall = read_rainfall_api(longitude, latitude)
        rain_sum = ""
        for rain in rainfall:
            rain_sum += str(rain)+", "
        await ctx.respond("Rain fall for the next 7 days looks like this: "+rain_sum)



def handle_prefix_commands(bot):

    embed = hikari.Embed()

    # Say hello to user specific with 
    @bot.command()
    @lightbulb.command("hello", "say hello to the bot")
    @lightbulb.implements(lightbulb.PrefixCommand)
    async def hello(ctx: lightbulb.Context) -> None:
        await ctx.respond("Hello! How are you?")

    # Greet user specified with command prefix
    @bot.command()
    @lightbulb.option("user", "User to greet", hikari.User)
    @lightbulb.command("greet", "Greets the specified user")
    @lightbulb.implements(lightbulb.PrefixCommand)
    async def greet(ctx: lightbulb.Context) -> None:
        await ctx.respond(f"Hello {ctx.options.user.mention}!")

    @bot.command()
    @lightbulb.command("embed", "Sends an embed in channel")
    @lightbulb.implements(lightbulb.PrefixCommand)
    async def embed_command(ctx: lightbulb.Context) -> None:
        embed = hikari.Embed(title="A Grogu Image", description="Embedding Grogu images since 2022...")
        embed.add_field("Grogu", "He's a jedi...we hope.")
        embed.set_thumbnail("https://unsplash.com/photos/ZFN6UNWhstI")
        embed.set_footer("This is Grogu")
        await ctx.respond(embed)  


def read_channel_messages(bot):

    @bot.listen(hikari.GuildMessageCreateEvent)
    async def on_message(event: hikari.GuildMessageCreateEvent):
        BOT_NAME = os.getenv("BOT_NAME")
        message_content = event.content
        print(event.content)
        if event.is_bot or not event.content:
            return
        if message_content.find("hey <@"+BOT_NAME) != -1:
            await event.message.respond(f"Hey back!")
    
    @bot.listen(hikari.GuildMessageCreateEvent)
    async def on_message(event: hikari.GuildMessageCreateEvent):
        message_content = event.content
        if event.is_bot or not event.content:
            return
        if message_content.find("jedi") != -1:
            await event.message.respond("I heard someone say Jedi!")


# Provides the Alexa Rank
# The lower the number, the better.
def verify_url(url):

    SEC_TRAILS_KEY = os.getenv("SEC_TRAILS_KEY")
    url = "https://api.securitytrails.com/v1/domain/"+url
    headers = {
        "Accept": "application/json",
        "APIKEY": SEC_TRAILS_KEY
    }
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    alexa_rank = json_data['alexa_rank']
    return alexa_rank


# API - NO KEY - https://open-meteo.com/
def read_rainfall_api(longitude, latitude):
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude="+latitude+"&longitude="+longitude+"&daily=rain_sum&temperature_unit=celsius&timezone=GMT")
    json_data = json.loads(response.text)
    daily = json_data['daily']
    rain_sum = daily['rain_sum']
    return rain_sum


def main():

    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    # COMMAND_GUILD_ID = int(os.getenv("COMMAND_GUILD_ID"))
    bot = lightbulb.BotApp(token=DISCORD_TOKEN, prefix="!", intents=hikari.Intents.ALL_UNPRIVILEGED, logs="INFO")
    
    read_channel_messages(bot)
    handle_prefix_commands(bot)
    handle_slash_commands(bot)
    bot.run()


if __name__ == "__main__":
    main()
