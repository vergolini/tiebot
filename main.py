import discord
import os
import requests
import random
import time
from discord.ext import commands
from flask import Flask
from threading import Thread

token = os.environ['env']
app = Flask('')
cooldown = False
cooldowntime = 0

robot = "hola si lees esto es que estoy vivo me llamo tiebot#4316 y no tengo nada que ver con tie no conozco a ese tipo somos personas completamente distintas haz .help para ver mis comandos adiós gracias"

# info de los comandos
info_prueba = ('Repite lo que dices, borrando el mensaje original')
alias_prueba = ('.prueba, .p')
uso_prueba = ('.prueba [mensaje]')

info_ayuda = ('Muestra esto')
alias_ayuda = ('.ayuda, .a, .?')
uso_ayuda = ('.ayuda')

info_agregar_mensaje = ('Agrega un mensaje a la lista de EZ')
alias_agregar_mensaje = ('.agregar_mensaje, .add')
uso_agregar_mensaje = ('.add [mensaje]')

info_quitar_mensaje = ('Agrega un mensaje de la lista de EZ')
alias_quitar_mensaje = ('.quitar_mensaje, .rem')
uso_quitar_mensaje = ('.rem [mensaje]')

info_ver_mensaje = ('Te enseña la lista (de EZ)')
alias_ver_mensaje = ('.ver_mensajes, .ver')
uso_ver_mensaje = ('.ver')

info_robot = ('Me manda a mi un mensaje especial ;)')
alias_robot = ('.robot, .r')
uso_robot = ('.r [mensaje]')

starter_ez_messages = ['I have really enjoyed playing with you!', 'I had something to say, then I forgot it.', "Why can't the Ender Dragon read a book? Because he always starts at the End.", 'Your clicks per second are godly. :o', 'Behold, the great and powerful, my magnificent and almighty nemesis!', 'In my free time I like to watch cat videos on youtube', 'Your personality shines brighter than the sun.', 'I have really enjoyed playing with you! <3', "Pineapple doesn't go on pizza!", 'If the world in Minecraft is infinite....how can the sun revolve around it?', 'Can you paint with all the colors of the wind', 'Doing a bamboozle fren.', 'Maybe we can have a rematch?', 'ILY<3', "Hello everyone! I'm an innocent player who loves everything Hypixel", 'I like minecraft pvp, but you are better than me!', 'If the Minecraft World is infinite, how does the sun spin around it?', 'Sometimes I try to say bad things, and then this happens.', 'I enjoy long walks on the beach and playing Hypixel', 'Welcome to the Hypixel zoo!', "Let's be friends instead of fighting okay?", 'I need help, teach me how to play!', 'I like to eat pasta, do you prefer nachos?', "You're a great person! Do you want to play some Hypixel games with me?", 'Your personality shines brighter than the sun.', 'Pls give me doggo memes!', 'Sometimes I sing soppy, love songs in the car', 'When I saw the guy with a potion I knew there was trouble brewing.', 'Hey Helper, how play game?', "Wait... this isn't what I typed!", 'I like pineapple on my pizza', 'When nothing is going right, go left.', 'What happens if I add chocolate milk to macaroni and cheese?', 'Anybody else really like Rick Astley?', 'I enjoy long walks on the beach and playing Hypixel', 'I had something to say, then I forgot it.', 'Please go easy on me, this is my first game!', 'You are very good at this game friend!', 'I heard you like minecraft, so I built a computer so you can minecraft, while minecrafting in your minecraft.', 'Blue is greener than purple for sure']

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    print('Iniciado sesión con {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=".ayuda"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "ez" in message.content.lower():
        await message.channel.send(random.choice(starter_ez_messages))

    await client.process_commands(message)

@client.command(aliases=['p'])
async def prueba(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete()

@client.command(aliases=['a', '?'])
async def ayuda(ctx):
    await ctx.send(f'Hola soy tiebot \nEstos son mis comandos: \n\n- Ayuda: {info_ayuda} \nAliases: {alias_ayuda} \nUso: {uso_ayuda} \n\n- Prueba: {info_prueba} \nAliases: {alias_prueba} \nUso: {uso_prueba}\n\n- Agregar mensaje: {info_agregar_mensaje} \nAliases: {alias_agregar_mensaje} \nUso: {uso_agregar_mensaje}\n\n- Quitar mensaje: {info_quitar_mensaje} \nAliases: {alias_quitar_mensaje} \nUso: {uso_quitar_mensaje}\n\n- Ver mensaje: {info_ver_mensaje} \nAliases: {alias_ver_mensaje} \nUso: {uso_ver_mensaje}\n\n- Robot: {info_robot} \nAliases: {alias_robot} \nUso: {uso_robot}')

@client.command(aliases=['add'])
async def agregar_mensaje(ctx, *, mensaje):
    starter_ez_messages.append(mensaje)
    await ctx.send("Mensaje agregado correctamente.")

@client.command(aliases=['rem'])
async def quitar_mensaje(ctx, *, mensaje):
    if mensaje in starter_ez_messages:
        starter_ez_messages.remove(mensaje)
        await ctx.send("Mensaje eliminado correctamente.")
    else:
        await ctx.send("El mensaje no existe en la lista.")

@client.command(aliases=['ver'])
async def ver_mensajes(ctx):
    mensaje_lista = "\n".join(starter_ez_messages)
    await ctx.send(f"Lista de mensajes:\n{mensaje_lista}")

@client.command(aliases=['r'])
async def robot(ctx, *, arg):
    global cooldowntime

    current_time = time.time()

    if current_time - cooldowntime < 60:
        remaining_time = round(60 - (current_time - cooldowntime))
        await ctx.send(f"Demasiado rápido. Espera {remaining_time} segundos.")
    else:
        cooldowntime = current_time
        global robot
        robot = arg
        await ctx.send("Mensaje enviado: https://tiebot2.vergolini.repl.co")
      
    if len(arg) > 30:
        await ctx.send("Mensaje demasiado largo. Máximo 30 caracteres.")

@app.route('/')
def home():
    response = requests.get('http://localhost:8080/get_robot')
    return response.text

@app.route('/get_robot')
def get_robot():
    return robot

def run():
    app.run(host='0.0.0.0', port=8080)

def run_discord():
    client.run(token)

def keep_alive():
    t1 = Thread(target=run)
    t2 = Thread(target=run_discord)
    t1.start()
    t2.start()

keep_alive()
