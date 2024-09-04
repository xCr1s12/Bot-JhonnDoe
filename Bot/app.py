import logging
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

load_dotenv()
my_secret = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

#############################################################

@bot.event
async def on_ready():
    print(f"{bot.user} ha conectado")



#evento cuando un usuario entra al sv (Terminado)
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1280585136286601328)
    if channel is not None:
        await channel.send(f"hola, {member.mention}!")
        
    guild = member.guild #esto es algo que tu hiciste pero lo movi para que se actualice junto con la entrada y salida
    await update_member_count(guild)


#Evento cuando alguien sale 
@bot.event
async def on_member_remove(member: discord.Member):
    await asyncio.sleep(2) 
    channel = bot.get_channel(1280585136286601328)
    await channel.send(f"Adios, {member.name}!")
    
    guild = member.guild #esto es algo que tu hiciste pero lo movi para que se actualice junto con la entrada y salida
    await update_member_count(guild)





# Función que actualiza el un canal que se llama "member-count" con el numero actual de miembros
@bot.event
async def update_member_count(guild):
    member_count = guild.member_count
    channel = bot.get_channel(1280588414588162121)   # Puedes cambiar el nombre del canal
    if channel:
        await channel.edit(name=f"Member Count: {member_count}")


#----------------------------------------------#
@bot.command(name= "saludo")
async def hola(ctx): #ctx es el parametro de contexto, es como lo que esta pasando en el momento y en donde esta funcionando el bot mas o menos
    
    member: discord.Member = ctx.author
    roles = [role.name for role in member.roles] 
    if "Persona" in roles:
        await ctx.send(f"Hola {member.name}")


# -------- Evento para los tickets

# ID del canal de "Tickets"
channel_id = 1281011438307250288

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

    channel = bot.get_channel(channel_id)
    if channel:
        mensaje = await channel.send("Reaciona con un 🎫 para abrir un ticket.")
        await mensaje.add_reaction("🎫")

# Evento para manejar la reaccion
@bot.event
async def on_reaction_add(reaction,user):
    if user.bot:
        return
    
    if str(reaction.emoji) == "🎫":
        guild = reaction.message.guild
        overwrites = {   
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

         # Crear el canal de ticket
        ticket_channel = await guild.create_text_channel(
            f'ticket-{user.name}',
            overwrites=overwrites
        )


bot.run(my_secret)