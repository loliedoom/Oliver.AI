#Import APIs
import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there!",
  "You are a great person!",
]

if "responding" not in db.keys():
  db["responding"] = True

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

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        msg = message.content

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

        if msg.startswith("0-del"):
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
            await message.channel.send("Responding enabled.")
          else:
            db["responding"] = False
            await message.channel.send("Responding off.")

        #Credits
        if message.content.lower().startswith("o-credits"):
            embedVar = discord.Embed(
                title="Credits",
                description="The people who made Oliver.AI possible. Proudly written in Python 3. Oliver.AI is open source, check out our GitHub!",
                color=0x83FFFF)
            embedVar.add_field(name="Development",
                               value="Anderson (Loliedoom#1111)",
                               inline=False)
            embedVar.add_field(name="Artistic Design",
                               value="Sir Lemon",
                               inline=False)
            embedVar.add_field(name="Inspiration",
                               value="My dearest friends.",
                               inline=False)
            embedVar.add_field(name="APIs",
                               value="Chatterbot, Discord.py",
                               inline=False)
            embedVar.add_field(name="GitHub",
                               value="https://github.com/loliedoom/Oliver.AI",
                               inline=False)
            await message.channel.send(embed=embedVar)

keep_alive()
client.run(os.getenv('TOKEN'))
