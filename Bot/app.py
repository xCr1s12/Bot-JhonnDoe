import logging
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
my_secret = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} ha conectado')

@bot.command(name="saludo")
async def hello(ctx):
    await ctx.send(f'Hola {ctx.author.name}, ¡bienvenido!')

@bot.command(name="patata")
async def patata(ctx):
    if ctx.author.role == 

bot.run(my_secret)