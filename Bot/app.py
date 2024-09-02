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
async def hola(ctx): #ctx es el parametro de contexto, es como lo que esta pasando en el momento y en donde esta funcionando el bot mas o menos
    member: discord.Member = ctx.author
    roles = [role.name for role in member.roles]
    if "Persona" in roles:
        await ctx.send(f"Hola {member.name}")

@bot.command(name = "Mute")

#Recuerda que siempre tienes que prender el bot moviendote hasta la carpeta script y poniendo activate en el cmd
#luego tienes que poner "py app.py"

bot.run(my_secret)