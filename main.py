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
bot = ChatBot('Oliver')
bot = ChatBot(
    'Oliver',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
)
bot = ChatBot(
    "Oliver",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        'chatterbot.logic.MathematicalEvaluation'
    ]
)

#Training Data
from chatterbot.trainers import ListTrainer

bot.set_trainer(ListTrainer)

#Important Stuff Below

sad_words = ["Fortnite", "Simp", "Sadness"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there!",
  "You are a great person!",
]

if "responding" not in db.keys():
  db["responding"] = False

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    await client.change_presence(activity=discord.Game('v0.0.2 | Need help? Try: o-help'))

    @client.event
    async def on_message(message):

        if message.author == client.user:
            return

        msg = message.content

        if msg.startswith("o/"):
          convo_message2 = msg.split("o/",1)[1]
          response2 = bot.get_response(convo_message2)
          await message.channel.send(response2)

        if message.content.lower().startswith('o-convo'):
          channel = message.channel
          BotUser = message.author
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

        if message.content.lower().startswith('o-train'):
          channel2 = message.channel
          BotUser2 = message.author
          await channel2.send("Enter the first message to act as the prompt.")
          def check(m):
              return m.author == BotUser2
          response2 = await client.wait_for("message",check=check)
          trainer1 = response2.content
          await channel2.send("Now enter the response Oliver will give.")
          def check(m):
              return m.author == BotUser2
          response3 = await client.wait_for("message",check=check)
          trainer2 = response3.content

          bot.train([
            (trainer1),
            (trainer2)
          ])

          await channel2.send("Oliver.AI is now successfully trained with the prompt: [" + response2.content + "] And the response: [" + response3.content + "]. Try using it with [o/] or [o-convo]")

        if message.content.lower().startswith('o-nuke'):
          channel3 = message.channel
          BotUser3 = message.author

          await channel3.send("You've activated the nuke function. Please input the message you want to spam:")
          def check(m):
              return m.author == BotUser3
          responsex2 = await client.wait_for("message",check=check)

          await channel3.send("How many times would you like to spam? 10 is the max unless you have a password. (Use an integer.)")
          def check(m):
              return m.author == BotUser3
          responsex3 = await client.wait_for("message",check=check)

          await channel3.send("If you have a password, please input it. If not, simply type whatever.")
          def check(m):
              return m.author == BotUser3
          responsex1 = await client.wait_for("message",check=check)
          if responsex1.content == "IThinkAndersonIsHotAndSexy":
            for x in range(0, int(responsex3.content)):
              await message.channel.send(responsex2.content)
          else:
            if int(responsex3.content) > 10:
              await message.channel.send("Since you didn't put the right password, the value you inputted is too high! Please use a number under 10.")

            if int(responsex3.content) <= 10:
              for x in range(0, int(responsex3.content)):
                await message.channel.send(responsex2.content)

        if message.content.lower().startswith('o-inspire'):
          quote = get_quote()
          await message.channel.send(quote)

        if db["responding"]:
          options = starter_encouragements
          if "encouragements" in db.keys():
            options = options + db["encouragements"]

          if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

        if msg.startswith("o-new"):
          encouraging_message = msg.split("o-new ",1)[1]
          update_encouragements(encouraging_message)
          await message.channel.send("New encouraging message added!")

        if msg.startswith("o-del"):
          encouragements = []
          if "encouragements" in db.keys():
            index = int(msg.split("o-del",1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
          await message.channel.send(encouragements)

        if msg.startswith("o-list"):
          encouragements = []
          if "encouragements" in db.keys():
            encouragements = db["encouragements"]
          await message.channel.send(encouragements)

        if msg.startswith("o-responding"):
          value = msg.split("responding ", 1)[1]

          if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding enabled. *Warning, this feature is part of a test build used for reference purpose, use this feature at your own risk.*")
          else:
            db["responding"] = False
            await message.channel.send("Responding off.")

        if message.content.lower().startswith("o-breathe"):

          embedVarM = discord.Embed(
                title="Mindfullness Exercise | Breathing",
                description="Let Oliver.AI guide you through a series of breathing exercises.",
                color=0x83FFFF)
          embedVarM.add_field(name="Starting in 5 seconds.",
                            value="This will only take 30 seconds.",
                            inline=False)

          embedVarN = discord.Embed(
              title="Mindfullness Exercise | Breathing",
              description="In a session...",
              color=0x83FFFF)
          embedVarN.add_field(name="Breathe In",
                          value="5 Rounds - 30 Seconds",
                          inline=False)

          embedVarN1 = discord.Embed(
              title="Mindfullness Exercise | Breathing",
              description="In a session...",
              color=0x83FFFF)
          embedVarN1.add_field(name="Breathe Out",
                          value="5 Rounds - 30 Seconds",
                          inline=False)

          embedVarD = discord.Embed(
                title="Mindfullness Exercise | Breathing",
                description="Complete.",
                color=0x83FFFF)
          embedVarD.add_field(name="That was awesome!",
                            value="Really, you did great. Hopefully you feel more relaxed. I'll be here if you need me again!",
                            inline=False)

          message = await message.channel.send(embed=embedVarM)

          time.sleep(5)
          for i in range(5):
            await message.edit(embed=embedVarN)
            time.sleep(3)
            await message.edit(embed=embedVarN1)
            time.sleep(3)
          await message.edit(embed=embedVarD)

        #Credits
        if message.content.lower().startswith("o-credits"):
            embedVar = discord.Embed(
                title="Oliver.AI v0.0.2 | Credits",
                description="The people who made Oliver.AI possible. Proudly written in Python 3. Oliver.AI is open source, check out our GitHub!",
                color=0x83FFFF)
            embedVar.add_field(name="Development",
                              value="Anderson (Loliedoom#2006)",
                              inline=False)
            embedVar.add_field(name="Artistic Design",
                              value="Sir Lemon",
                              inline=False)
            embedVar.add_field(name="Inspiration",
                              value="My dearest friends.",
                              inline=False)
            embedVar.add_field(name="APIs",
                              value="Chatterbot, Discord.py, ZenQuotes.io",
                              inline=False)
            embedVar.add_field(name="GitHub",
                              value="https://github.com/loliedoom/Oliver.AI",
                              inline=False)
            embedVar.add_field(name="Privacy Warning",
                              value="Every message sent to Oliver.AI will be processed by its AI and will be stored on its database. Oliver.AI will not record anything other than what it's called to record. Make sure you don't leak any personal information while using Oliver.AI.",
                              inline=False)
            await message.channel.send(embed=embedVar)

        #Request Help
        if message.content.lower().startswith("o-help"):
            embedVar2 = discord.Embed(
              title = "Oliver.AI v0.0.2 | Help",
              description = "Need help using Oliver.AI? Don't worry, we got you.", color=0x83FFFF)
            embedVar2.add_field(name="Credits and Settings",
                              value="Use [o-help] to open this panel. Use [o-credits] to get insight on the creators of Oliver.AI",
                              inline=False)
            embedVar2.add_field(name="Conversation [AI-Assisted]",
                              value="Use [o/] followed by your prompt to make a one-time request to Oliver's chat engine. Use [o-convo] to lock into a conversation. Use [o-train] to be tailor Oliver to certain responses. Don't worry, it will guide you through it.",
                              inline=False)
            embedVar2.add_field(name="Mindfulless",
                              value="Use [o-inspire] to get an inspring quote. Use [o-breathe] to start a breathing exercise.",
                              inline=False)
            embedVar2.add_field(name="Fun Commands",
                              value="Use [o-nuke] to flood a chat with your desired text. A password is required for values over 10.",
                              inline=False)
            embedVar2.add_field(name="[Deprecated] Pre-set messages.",
                              value="Use [o-list] to get a list of messages encoded. Use [o-new] to add a new message. Use [o-del #] to delete a message. Use [o-responding true/false] to toggle responding. Say any of these 3 words: Fortnite, Simp, Sadness, to trigger the response. *This feature is deprecated and is no longer supported, this is here for reference. Although, it still might work.*",
                              inline=False)

            await message.channel.send(embed=embedVar2)

keep_alive()
client.run(os.getenv('TOKEN'))