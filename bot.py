import discord
from discord.ext import commands
from tts import TTS

TOKEN = "TOKEN HERE"
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)
tts = TTS()
vc = None

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_message(message): #TODO: Optimize this
    if message.author.bot:
        return
    global vc
    if message.content == "!enable":
        if message.author.voice == None:
            await message.channel.send("You are not in a voice channel")
        elif vc == None:
            vc = await message.author.voice.channel.connect()
            await message.channel.send("TTS has been enabled")
        else:
            await message.channel.send("TTS is already enabled")
    elif message.content == "!disable":
        if vc != None:
            await vc.disconnect()
            vc = None
            await message.channel.send("TTS has been disabled")
        else:
            await message.channel.send("TTS is not enabled")
    elif message.content == "!move":
        if vc == None:
            await message.channel.send("TTS is not enabled")
        elif vc != message.author.voice.channel:
            await vc.disconnect()
            vc = await message.author.voice.channel.connect()
            await message.channel.send("Moved channels")
        else:
            await message.channel.send("Already in your current channel")
    elif message.author.voice != None and message.author.voice.self_mute and vc != None:
        tts.speak(message.content)
        for x in client.voice_clients:
            if x.guild == message.guild:
                vc.stop()
        source = discord.FFmpegPCMAudio(source="output.wav", executable="TTSDiscordBot/ffmpeg.exe")
        vc.play(source)
    
client.run(TOKEN)
