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






# -------- Evento para los tickets

# ID del canal de "Tickets"
channel_id = 1281011438307250288

@bot.event
async def on_ready():

    channel = bot.get_channel(channel_id)
    if channel:
        mensaje = await channel.send("Reaciona con un 🎫 para abrir un ticket.")
        await mensaje.add_reaction("🎫")


# Evento para manejar la reaccion
@bot.event
async def on_reaction_add(reaction,user):
    guild = reaction.message.guild #ESTO DE ACA REUNE LOS DATOs
    category = discord.utils.get(guild.categories, id=1281109607162445824)#Esto guarda la info de la categoria a la q se va enviar el ticket
    num_Ticket = len(category.channels) # y esto cuenta los canales en la categoria
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
            f'ticket-{num_Ticket}',
            overwrites=overwrites,
            category = category
        )
############## sin terminar

@bot.command(name= "saludo")
async def hola(ctx): #ctx es el parametro de contexto, es como lo que esta pasando en el momento y en donde esta funcionando el bot mas o menos
    
    member: discord.Member = ctx.author
    roles = [role.name for role in member.roles] 
    if "Persona" in roles:
        await ctx.send(f"Hola {member.name}")


@bot.command(name = "Bdelete")
@commands.has_permissions(manage_messages=True)#permiso unico admins

async def bdelete(ctx, count: int):
    
    await ctx.channel.purge(limit=count + 1)#Borrar :v 

"""@bot.event
async def on_message(message):
    Bad_words = ["puto"]
    if message.author == bot.user:
        return 
    for i in message.content:
        if i in Bad_words[0]:
            await message.delete

"""

# Evento "Borrar imágen enviada en canal erróneo"
@bot.event
async def on_message(message):
    imagenes_channel_id = 1281678969963282492 # Id del canal "Imagenes" (id del Server de prueba)

    if message.author.bot: # esto hace que si el autor del mensaje es el bot, no hace nada
        return
    
    if message.attachments: # <-- Verifica si el mensaje contiene un "archivo adjunto"
        
        if message.channel.id != imagenes_channel_id: # <-- Verifica si el canal no es el de "imagenes"
            await message.delete() # <-- elimina el mensaje 
                                                                                                            # Mensaje de advertencia, se borra despues de 10 segundos.
            await message.channel.send(f"{message.author.mention}, porfavor envía las imágenes en el canal <#{imagenes_channel_id}>.", delete_after=10) 


bot.run(my_secret)