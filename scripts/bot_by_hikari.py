import random
import hikari
import os
from dotenv import load_dotenv
import requests

def check_discord_messages(bot):

    BOT_NAME = os.getenv("BOT_NAME")
    @bot.listen()
    async def handle_messages(event: hikari.GuildMessageCreateEvent) -> None:
       
        message_content = event.content.lower()
        print(message_content)

        if event.is_bot or not event.content:
            return
        
        if message_content.find("hey <@"+BOT_NAME) != -1 or message_content.find("hello <@"+BOT_NAME) != -1:
            user = str(event.author)
            # Retrieve the user that mentioned
            await event.message.respond("Hey "+user+" how are you?")
        
        if message_content.find("bonjour <@"+BOT_NAME) != -1:
            user = str(event.author)
            # Retrieve the user that mentioned
            await event.message.respond("Bonjour "+user+", ça va?")

        if message_content.find("joke") != -1:
            jokes = [
                "Why did the programmer leave the camping trip early?\n🥁 Because there were too many bugs! 🐛 🐛 🐛",
                "What did the hacker's out of office message say?\n🥁 Gone phishing. 🎣 🎣 🎣",
                "What do you call a turtle that surfs the Dark Web?\n🥁 A TORtoise. 🧅 🐢 🧅 🐢 🧅 🐢 ",
                "What's a hacker's favourite season?\n🥁 Phishing season. 🎣 🎣 🎣 ",
                "What’s the best way to catch a runaway robot?\n🥁 Use a botnet. 🤖 🥅 ",
                "An SQL statement walks into a bar and sees two tables. It approaches and asks…\n🥁 May I join you? 🍸 🍸 🍸"
            ]
            random_num = random.randrange(0, len(jokes)-1)
            await event.message.respond("Did you say joke?! Here's a joke:\n"+jokes[random_num])

        if message_content.find("cat") != -1:
            cat_request = "https://cataas.com/cat/gif"
            cat_response = requests.get(cat_request)
            await event.message.respond("Is someone talking about cats?! I love cats! ❤️ 🐈 \nHere's a random cat gif: "+cat_response.url)

        if message_content.find("jedi") != -1:
            yodas_wise_words = [
                "A Jedi uses the Force for knowledge and defense, never for attack.",
                "A Jedi’s strength flows from the Force.",
                "Luminous beings are we…not this crude matter.",
                "Named must your fear be before banish it you can.",
                "Difficult to see. Always in motion is the future."
            ]
            random_num = random.randrange(0, len(yodas_wise_words)-1)
            await event.message.respond(yodas_wise_words[random_num])


def configure_slash_commands(bot, COMMAND_GUILD_ID):

    @bot.listen()
    async def register_commands(event: hikari.StartingEvent) -> None:
        application = await bot.rest.fetch_application()

        commands = [
            bot.rest.slash_command_builder("help", "Get some help with bot commands."),
            bot.rest.slash_command_builder("joke", "Tell you a joke"),
            # bot.rest.slash_command_builder("ephemeral", "Send a very secret message."),
        ]

        await bot.rest.set_application_commands(
            application=application.id,
            commands=commands,
            guild=COMMAND_GUILD_ID,
        )


def handle_slash_commands(bot):
    
    @bot.listen()
    async def handle_interactions(event: hikari.InteractionCreateEvent) -> None:

        if not isinstance(event.interaction, hikari.CommandInteraction):
            # only listen to command interactions, not others!
            return
        if event.interaction.command_name == "help":
            await event.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                "/help to display help menu\n /joke to display a joke ",
            )
        elif event.interaction.command_name == "joke":
            jokes = [
                "Why did the programmer leave the camping trip early?\n🥁 Because there were too many bugs! 🐛 🐛 🐛",
                "What did the hacker's out of office message say?\n🥁 Gone phishing. 🎣 🎣 🎣",
                "What do you call a turtle that surfs the Dark Web?\n🥁 A TORtoise. 🧅 🐢 🧅 🐢 🧅 🐢 ",
                "What's a hacker's favourite season?\n🥁 Phishing season. 🎣 🎣 🎣 ",
                "What’s the best way to catch a runaway robot?\n🥁 Use a botnet. 🤖 🥅 ",
                "An SQL statement walks into a bar and sees two tables. It approaches and asks…\n🥁 May I join you? 🍸 🍸 🍸"
            ]
            random_num = random.randrange(0, len(jokes)-1)
            await event.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                jokes[random_num],
            )


        # elif event.interaction.command_name == "sherlock":

def main():

    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    COMMAND_GUILD_ID = int(os.getenv("COMMAND_GUILD_ID"))
    bot = hikari.GatewayBot(token=DISCORD_TOKEN)

    check_discord_messages(bot)  
    configure_slash_commands(bot, COMMAND_GUILD_ID)
    handle_slash_commands(bot)

    bot.run()


if __name__ == "__main__":
    main()
