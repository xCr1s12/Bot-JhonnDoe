from colorama import Fore, Back, Style
import logging
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import asyncio


#Carga el token del bot 
load_dotenv()
my_secret = os.getenv("TOKEN")

#Permisos para el bot
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

#bot xd 
bot = commands.Bot(command_prefix="!", intents=intents)

###########################################################
"""
#####AQUI COMIENZA LA SECCION DE EVENTOS DE  EL BOT#####

"""

###################################################################################

"""
Este evento interactua cuando el bot enciende y avisa ala consola, tambien gestiona el mensaje de los tickets  
"""
@bot.event
async def on_ready():
    print(Fore.GREEN + Back.WHITE + Style.BRIGHT + f"{bot.user} ha conectado" + Style.RESET_ALL)

    channel = bot.get_channel(1281011438307250288)
    if channel:
        mensaje = await channel.send("Reaciona con un 🎫 para abrir un ticket.")
        await mensaje.add_reaction("🎫")


###################################################################################

"""
A conjunto con el primer evento este reacciona para crear un canal privado en el cual solo el usuario y los moderadores 
pueden acceder

"""
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
####################################################################################

"""
evento de moderacion automatica para revisar si el mensaje contiene alguna mala palabra.
################## EL DICCIONARIO DE MALAS PALABRAS 3000 ###############################
"""
@bot.event
async def on_message(message):
    Bad_words = ["puto"]
    if message.author == bot.user:
        return 
    if any(bad_word in message.content.lower() for bad_word in Bad_words) and not message.author.guild_permissions.administrator:
        await message.delete()
    await bot.process_commands(message)
####################################################################################
"""
Función que actualiza un canal "member count" con el numero actual de miembros

"""
@bot.event
async def update_member_count(guild):
    member_count = guild.member_count
    channel = bot.get_channel(1280588414588162121)   # Puedes cambiar el nombre del canal
    if channel:
        await channel.edit(name=f"Member Count: {member_count}")
"""
saluda a miembros nuevos :3 
"""
    # URL de la imagen de bienvenida (debes reemplazarla con la tuya)
BANNER = "logo.png"

# ID del canal donde quieres que se envíen los mensajes de bienvenida
ID_CANAL_BIENVENIDA = 1280585136286601328  # Reemplaza con el ID de tu canal

@bot.event
async def on_member_join(member):
    # Obtener el canal de bienvenida
    channel = bot.get_channel(ID_CANAL_BIENVENIDA)
    if channel:
        # Enviar mensaje de bienvenida con una mención al nuevo usuario
        await channel.send(f"¡Bienvenido/a, {member.mention}! 🎉 Estamos felices de tenerte aquí.")

        # Enviar el banner de bienvenida
        await channel.send(BANNER)

"""
Despide a antiguos usuarios
""" 
@bot.event
async def on_member_remove(member: discord.Member):
    await asyncio.sleep(2) 
    channel = bot.get_channel(1280585136286601328)
    await channel.send(f"Adios, {member.name}!")
    
    guild = member.guild #esto es algo que tu hiciste pero lo movi para que se actualice junto con la entrada y salida
    await update_member_count(guild)
#####################################################################################
"""
evento de automoderacion 
elimina fotos que no han sido enviadas en el canal correcto
"""
@bot.event
async def on_message(message):
    imagenes_channel_id = 1281678969963282492 # Id del canal "Imagenes" (id del Server de prueba)
    if message.author.bot: # esto hace que si el autor del mensaje es el bot, no hace nada
        return

    if message.attachments: # <-- Verifica si el mensaje contiene un "archivo adjunto"
        
        if message.channel.id != imagenes_channel_id and not message.author.guild_permissions.administrator: # <-- Verifica si el canal no es el de "imagenes"
            await message.delete() # <-- elimina el mensaje 
             # Mensaje de advertencia, se borra despues de 10 segundos.
            await message.channel.send(f"{message.author.mention}, porfavor envía las imágenes en el canal <#{imagenes_channel_id}>.", delete_after=10) 

    await bot.process_commands(message)

#####################################################################################
"""
Aca va el comando de saludo del bot
"""











#####################################################################################
"""
Aqui comienza la seccion de comandos
"""

#####################################################
"""
!saludo #Saluda al usuario (comando de prueba :3)
"""
@bot.command(name= "saludo")
async def hola(ctx): #ctx es el parametro de contexto, es como lo que esta pasando en el momento y en donde esta funcionando el bot mas o menos
    
    member: discord.Member = ctx.author
    roles = [role.name for role in member.roles] 
    if "Persona" in roles:
        await ctx.send(f"Hola {member.name}")

#####################################################
"""
!clc "cantiad a borrar" borra mensajes para limpiar un chat (es solo para mantener un poco de limpieza :3)
"""
@bot.command(name = "clc")
@commands.has_permissions(manage_messages=True)#permiso unico admins

async def clc(ctx, count: int):
    await ctx.channel.purge(limit=count + 1)#Borrar :v 

bot.run(my_secret)

