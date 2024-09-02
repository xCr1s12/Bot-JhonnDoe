import logging
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
my_secret = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} ha conectado")




@bot.command(name= "saludo")
async def hola(ctx):
    member: discord.Member = ctx.author
    roles = [role.name for role in member.roles]
    if "Persona" in roles:
        await ctx.send(f"Hola {member.name}")



bot.run(my_secret)