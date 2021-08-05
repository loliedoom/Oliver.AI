#Import APIs and Libraries

import discord
import os
import requests
import json
import random
import time
from replit import db
from keep_alive import keep_alive

client = discord.Client()

#Import Chatterbot API
from chatterbot import ChatBot
bot = ChatBot(
    'Oliver',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    database_uri='mongodb+srv://Loliedoom:KllGR6nKkv9sUsPC@olivercluster.zgijd.mongodb.net/OliverCluster?retryWrites=true&w=majority'
)

from chatterbot.trainers import ChatterBotCorpusTrainer

bot.set_trainer(ChatterBotCorpusTrainer)

bot.train(
    "chatterbot.corpus.english",
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)

#Global Variables

Version = "v0.0.4 Exodus"

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

#Start Bot

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    await client.change_presence(activity=discord.Game(str(Version) + ' | Need help? Try: o-help'))
    
    @client.event
    async def on_message(message):

        if message.author == client.user:
            return

        msg = message.content

        #Global Variables
        channel = message.channel
        BotUser = message.author

        ThinkingResponse0 = "*Hold on, I'm thinking!*"
        ThinkingResponse1 = "*Just a sec...*"
        ThinkingResponse2 = "*Hm... Working on it.*"

        if msg.startswith("o/"):
          convo_message2 = msg.split("o/",1)[1]

          randomvalue = (random.randint(0,2))

          if randomvalue == (0):
            await message.channel.send(ThinkingResponse0)
          if randomvalue == (1):
            await message.channel.send(ThinkingResponse1)
          if randomvalue == (2):
            await message.channel.send(ThinkingResponse2)

          response = bot.get_response(convo_message2)
          await message.channel.send(response) 

        if message.content.lower().startswith('o-convo'):
          await channel.send("Conversation locked with " + str(BotUser) + ". Type o-quit to exit.")
          while True:
            def check(m):
                return m.author == BotUser or m.content.lower().startswith('o-quit')
            response = await client.wait_for("message",check=check)
            botresponse = response.content
            botfeedback = bot.get_response(botresponse)
            if response.content.startswith("o-quit"):
                await channel.send("Conversation ended with " + str(BotUser))
                break
            else:
                await message.channel.send(botfeedback)

        if message.content.lower().startswith('o-imagine'):
          await channel.send("Type in something to imagine, and I'll give you an image.")
          def check(m):
              return m.author == BotUser
          response = await client.wait_for("message",check=check)
          import requests
          import re
          r = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
              'text': str(response.content),
            },
            headers={'api-key': 'f07cc451-41d9-4cd4-9ce7-630b38d2fa7c'}
          )
          imagineoutput = str(r.json())
          imagineoutput2 = (re.search("(?P<url>https?://[^\s]+)", imagineoutput).group("url"))
          imagineoutput3 = imagineoutput2[:-2]
          await channel.send(imagineoutput3)

        if msg.startswith("oimagine/"):
          imagineprompt = msg.split("oimagine/",1)[1]
          import requests
          import re
          r = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
              'text': str(imagineprompt),
            },
            headers={'api-key': 'f07cc451-41d9-4cd4-9ce7-630b38d2fa7c'}
          )
          imagineoutput = str(r.json())
          imagineoutput2 = (re.search("(?P<url>https?://[^\s]+)", imagineoutput).group("url"))
          imagineoutput3 = imagineoutput2[:-2]
          await channel.send("Here's your image! " + str(BotUser) + " | " + str(imagineoutput3))

        if message.content.lower().startswith('o-train'):

          await channel.send("Enter the first message to act as a prompt for Oliver to listen for.")
          def check(m):
              return m.author == BotUser
          response1 = await client.wait_for("message",check=check)
          trainer1 = response1.content
          await channel.send("Now enter the response Oliver will give when the prompt is given.")
          def check(m):
              return m.author == BotUser
          response2 = await client.wait_for("message",check=check)
          trainer2 = response2.content

          bot.train([
            (trainer1),
            (trainer2)
          ])

          await channel.send("Oliver.AI is now successfully trained with the prompt: [" + response1.content + "] And the response: [" + response2.content + "]. Try using it with [o/] or [o-convo]")

        #Fun Commands
        if message.content.lower().startswith('o-nuke'):
          await channel.send("What do you want to spam?")
          def check(m):
              return m.author == BotUser
          responsex = await client.wait_for("message",check=check)

          await channel.send("How many times would you like to spam? Five is the max unless you have administrator permissions. (Use an integer number please!)")
          def check(m):
              return m.author == BotUser
          responsex1 = await client.wait_for("message",check=check)

          if message.author.guild_permissions.administrator:
            if int(responsex1.content) <= 500:
              for x in range(0, int(responsex1.content)):
                await message.channel.send(responsex.content)
            if int(responsex1.content) > 500:
              await message.channel.send("That number is too large! The maximum regardless of permission is 500. Please try again with a number equivalent to 500 or less.")
          else:
            if int(responsex1.content) > 5:
              await message.channel.send("Since you aren't an administrator in this server,you are unable to send more than five messages. Try again with a number smaller than six.")

            if int(responsex1.content) <= 5:
              for x in range(0, int(responsex1.content)):
                await message.channel.send(responsex.content)
        
        #Utility
        if message.content.lower().startswith('o-debug'):
          await message.channel.send("Bot Latency: " + str(client.latency * 1000) + "ms ""\nBot Version: " + (Version) + "\nGuild: " + (BotUser.guild.name) + "\nMessage Author: " + str(BotUser))

        #Mindfullness
        if message.content.lower().startswith("o-breathe"):
          embedVarBreatheStarter = discord.Embed(
                title="Mindfullness Exercise | Breathing",
                description="Let Oliver.AI guide you through a series of breathing exercises.",
                color=0x83FFFF)
          embedVarBreatheStarter.add_field(name="Starting in 5 seconds.",
                            value="This will only take 30 seconds.",
                            inline=False)

          embedVarBreathe1 = discord.Embed(
              title="Mindfullness Exercise | Breathing",
              description="In a session...",
              color=0x83FFFF)
          embedVarBreathe1.add_field(name="Breathe In",
                          value="5 Rounds - 30 Seconds",
                          inline=False)

          embedVarBreathe2 = discord.Embed(
              title="Mindfullness Exercise | Breathing",
              description="In a session...",
              color=0x83FFFF)
          embedVarBreathe2.add_field(name="Breathe Out",
                          value="5 Rounds - 30 Seconds",
                          inline=False)

          embedVarBreathe3 = discord.Embed(
                title="Mindfullness Exercise | Breathing",
                description="Complete.",
                color=0x83FFFF)
          embedVarBreathe3.add_field(name="That was awesome!",
                            value="Really, you did great. Hopefully you feel more relaxed. I'll be here if you need me again!",
                            inline=False)

          message = await message.channel.send(embed=embedVarBreatheStarter)

          time.sleep(5)
          for i in range(5):
            await message.edit(embed=embedVarBreathe1)
            time.sleep(3)
            await message.edit(embed=embedVarBreathe2)
            time.sleep(3)
          await message.edit(embed=embedVarBreathe3)

        if message.content.lower().startswith('o-inspire'):
          quote = get_quote()
          await message.channel.send(quote)

        #Credits
        if message.content.lower().startswith("o-credits"):
            embedc = discord.Embed(
                title= (str(Version) + " | Credits"),
                description="The people who made Oliver.AI possible. Proudly written in Python 3. Oliver.AI is open-source, check out our GitHub!",
                color=0x83FFFF)
            embedc.add_field(name="Development",
                              value="Anderson (Loliedoom#5314)",
                              inline=False)
            embedc.add_field(name="Inspiration",
                              value="My Friends",
                              inline=False)
            embedc.add_field(name="APIs and Libraries Used",
                              value="Chatterbot, Discord.py, ZenQuotes.io, DeepAI Text To Image by Scott Ellison Reed",
                              inline=False)
            embedc.add_field(name="GitHub",
                              value="https://github.com/loliedoom/Oliver.AI",
                              inline=False)
            embedc.add_field(name="Servers",
                              value="MongoDB Cluster: Azure Servers in Virginia \nRunning on Repl.it servers",
                              inline=False)
            embedc.set_footer(text="Every message sent to Oliver.AI will be processed by its AI and will be stored on its database. Oliver.AI will not record anything other than what it's called to record. Make sure you don't leak any personal information while using Oliver.AI.")
            await message.channel.send(embed=embedc)

        #Request Help
        if message.content.lower().startswith("o-help"):
            embedh = discord.Embed(
              title = (str(Version) + " | Help"),
              description = "Need help using Oliver.AI? Don't worry, we got you.", color=0x83FFFF)
            embedh.add_field(name="Credits and Settings",
                              value="Use [o-help] to open this panel. Use [o-credits] to get insight on the creators of Oliver.AI",
                              inline=False)
            embedh.add_field(name="Conversation [AI-Assisted]",
                              value="Use [o/] followed by your prompt to make a one-time request to Oliver's chat engine. Use [o-convo] to lock into a conversation.",
                              inline=False)
            embedh.add_field(name="Emotional Support [AI-Assisted]",
                              value="Use [o-support] to switch to Oliver's emotional support database. This command works similarily to [o-convo], but doesn't use the general response engine.",
                              inline=False)
            embedh.add_field(name="Imagine [AI-Assisted]",
                              value="Use [o-imagine] to generate an image out of text. You can also do [oimagine/] following by the prompt to make a request in one line. For information on the API used, use [o-credits].",
                              inline=False)
            embedh.add_field(name="Mindfulless",
                              value="Use [o-inspire] to get an inspring quote. Use [o-breathe] to start a breathing exercise.",
                              inline=False)
            embedh.add_field(name="Fun Commands",
                              value="Use [o-nuke] to flood a chat with your desired text. A password is required for values over 5.",
                              inline=False)
            embedh.add_field(name="Utility Commands",
                              value="Use [o-debug] to get details such as latency, guild name, author name, and version number. ",
                              inline=False)
            await message.channel.send(embed=embedh)

keep_alive()
client.run(os.getenv('TOKEN'))