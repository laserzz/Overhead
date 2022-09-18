import discord
import motor.motor_asyncio
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGOSTRING"))

maindb = client.overhead
coll = maindb["applications"]
apdcoll = maindb["appdata"]
vcoll = maindb["verify"]
apucoll = maindb["appusers"]
vdcoll = maindb["vdata"]
vmcoll = maindb["verifymodal"]
vucoll = maindb["vusers"]
ecoll = maindb["entry"]

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.guilds = True

bot = discord.Bot(intents=intents)

for files in os.listdir("./cogs"):
    if files.endswith(".py"):
        cogf = files[:-3]
        try:
            bot.load_extension(f"cogs.{cogf}")
            print(f"{cogf} initialized!")
        except Exception as e:
            print(e)

@bot.event
async def on_ready():
    activity = discord.Game(name="Staff Application Manager")
    print(f"logged in as {bot.user}")
    await asyncio.sleep(20)
    await bot.change_presence(activity=activity)

bot.run(os.getenv("TOKEN"))