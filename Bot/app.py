import logging
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
my_secret = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print(f"{bot.user} ha conectado")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1278837620108955791)
    if channel is not None:
        await channel.send(f"hola, {member.mention}!")



@bot.command(name= "saludo")
async def hola(ctx): #ctx es el parametro de contexto, es como lo que esta pasando en el momento y en donde esta funcionando el bot mas o menos
    
    member: discord.Member = ctx.author
    roles = [role.name for role in member.roles]
    if "Persona" in roles:
        await ctx.send(f"Hola {member.name}")

#Recuerda que siempre tienes que prender el bot moviendote hasta la carpeta script y poniendo activate en el cmd
#luego tienes que poner "py app.py"

# evento cuando un miembro entra al server
@bot.event
async def on_member_join(member):
    guild = member.guild
    await update_member_count(guild)

# evento cuando un miembro se va del server
@bot.event
async def on_member_remove(member):
    guild = member.guild
    await update_member_count(guild)

# Función que actualiza el un canal que se llama "member-count" con el numero actual de miembros
async def update_member_count(guild):
    member_count = guild.member_count
    channel = discord.utils.get(guild.channels, name="member-count")  # Puedes cambiar el nombre del canal
    if channel:
        await channel.edit(name=f"Member Count: {member_count}")





bot.run(my_secret)