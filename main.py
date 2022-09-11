import discord
import motor.motor_asyncio
from dotenv import load_dotenv
import os
from discord.ext import commands

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

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)

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
    print(f"logged in as {bot.user}")

bot.run(os.getenv("TOKEN"))