import discord
from discord.ext import commands
from discord.utils import get
import time
import asyncio
import random
import os



print('"discordMusicBot.py" script started!')
# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
token = ""  # Discord Bot Token
musicDirectory = r""  # Example: C:\Users\User\Desktop\Songs

commandPrefix = "!"  # Command Prefix
defaultVolumeValue = 0.07  # Default 0.07



# ------------------------------------------------------------
# Basic setup and Functions
# ------------------------------------------------------------
bot = commands.Bot(command_prefix=commandPrefix)
bot.remove_command("help")

songTitle = "None"
playerStopped = False

def message(msg):
    return discord.Embed(description=msg, color=0x007fff)



# ------------------------------------------------------------
# Confirm that the bot is online
# ------------------------------------------------------------
@bot.event
async def on_ready():
    print("Logged on as", bot.user)



# ------------------------------------------------------------
# Test command
# ------------------------------------------------------------
@bot.command()
async def test(content):
    await content.send("Things work!")



# ------------------------------------------------------------
# Help message
# ------------------------------------------------------------
@bot.command()
async def help(content):
    print("[*] " + content.message.author.name + " issued: " + commandPrefix + "help | Displays the help message")

    help = """**Display this message:**
           ```!help```
           **Show configuration:**
           ```!config```
           **Add the Music Bot to your voice channel:**
           ```!join```
           **Remove the Music Bot from your voice channel:**
           ```!leave```
           **Start playing a random song from the playlist:**
           ```!play```
           **Pause the music:**
           ```!pause```
           **Resume the music:**
           ```!resume```
           **Stop the music:**
           ```!stop```
           **Skip the song:**
           ```!skip```
           **Display song name:**
           ```!song```"""

    helpMessage = discord.Embed(title="Music Bot Commands", description=help, color=0x007fff)
    await content.send(embed=helpMessage)



# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
@bot.command()
async def config(content):
    print("[*] " + content.message.author.name + " issued: " + commandPrefix + "config | Displays the configuration")

    config = "**Command Prefix: \n**```" + str(commandPrefix) + "```\n"
    config = config + "**Volume: \n**```" + str(defaultVolumeValue) + " (Default: 0.07)```\n"
    config = config + "**Music Directory: \n**```" + str(musicDirectory) + "```\n"
    config = config + "**Current songs in directory: \n**```" + str(len([name for name in os.listdir(musicDirectory)])) + "```\n"

    configMessage = discord.Embed(title="Configuration", description=config, color=0x007fff)
    await content.send(embed=configMessage)



# ------------------------------------------------------------
# Adds the Music Bot to the senders voice channel
# ------------------------------------------------------------
@bot.command()
async def join(content):
    print("[*] " + content.message.author.name + " issued: " + commandPrefix + "join | Add the Music Bot to your voice channel")
    
    try:
        channel = content.message.author.voice.channel

        if(content.voice_client is not None):
            await content.voice_client.move_to(channel)
        else:
            await channel.connect()
            await content.send(embed=message(str(bot.user.name) + " connected to " + str(channel) + "."))

    except:
        await content.send(embed=message("You are not connnected to a voice channel, please connect to one."))



# ------------------------------------------------------------
# Removes the Music Bot from the senders voice channel
# ------------------------------------------------------------
@bot.command()
async def leave(content):
    print("[*] " + content.message.author.name + " issued: " + commandPrefix + "leave | Remove the Music Bot from your voice channel")

    global songTitle
    global playerStopped
    
    channel = content.message.author.voice.channel
    playerStopped = True
    content.voice_client.stop()
    songTitle = "None"

    if(content.voice_client == None):
        await content.send(embed=message(str(bot.user.name) + " is not connected to any voice channel."))
    else:
        await content.voice_client.disconnect()
        await content.send(embed=message(str(bot.user.name) + " disconnected from " + str(channel) + "."))



# ------------------------------------------------------------
# Start playing a random song from the playlist
# ------------------------------------------------------------
@bot.command()
async def play(content):
    print("[*] " + content.message.author.name + " issued: " + commandPrefix + "play | Start playing a random song from the playlist")

    global playerStopped

    def playSong():
        global playerStopped

        if(playerStopped == False):
            global songTitle

            randomSong = random.choice(os.listdir(musicDirectory))
            songTitle = randomSong

            fileSource = musicDirectory + "\\" + songTitle
            fileConfig = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(fileSource), volume=defaultVolumeValue)
            content.voice_client.play(fileConfig, after=lambda e: playSong())


    if(content.voice_client.is_playing()):
        await content.send(embed=message("Music Player is already playing."))
    else:
        playerStopped = False
        await content.send(embed=message("Music Player has been started."))
        playSong()



# ------------------------------------------------------------
# Pause the music
# ------------------------------------------------------------
@bot.command()
async def pause(content):
    print("[*] " + content.message.author.name + " issued: " + commandPrefix + "pause | Pause the music")

    if(content.voice_client.is_paused()):
        await content.send(embed=message("Music Player has already been paused."))
    else:
        content.voice_client.pause()
        await content.send(embed=message("Music Player has been paused."))



# ------------------------------------------------------------
# Resume the music
# ------------------------------------------------------------
@bot.command()
async def resume(content):
    print("[*] " + content.message.author.name + " issued: " + commandPrefix + "resume | Resume the music")

    if(content.voice_client.is_playing()):
        await content.send(embed=message("Music Player is already playing."))
    else:
        content.voice_client.resume()
        await content.send(embed=message("Music Player has been resumed."))



# ------------------------------------------------------------
# Stop the music
# ------------------------------------------------------------
@bot.command()
async def stop(content):
    print("[*] " + content.message.author.name + " issued: " + commandPrefix + "stop | Stop the music")

    global songTitle
    global playerStopped
    
    playerStopped = True
    content.voice_client.stop()
    songTitle = "None"

    await content.send(embed=message("Music Player has been stopped."))



# ------------------------------------------------------------
# Skip the song
# ------------------------------------------------------------
@bot.command()
async def skip(content):
    print("[*] " + content.message.author.name + " issued: " + commandPrefix + "skip | Skip the song")

    if(content.voice_client.is_playing()):
        content.voice_client.stop()
        await content.send(embed=message("The song has been skipped."))
    else:
        await content.send(embed=message("There is currently no song playing"))



# ------------------------------------------------------------
# Display song name
# ------------------------------------------------------------
@bot.command()
async def song(content):
    print("[*] " + content.message.author.name + " issued: " + commandPrefix + "song | Display song name")

    global songTitle

    if(songTitle == "None"):
        await content.send(embed=message("There is currently no song playing."))
    else:
        await content.send(embed=message("Currently playing: \"" + songTitle[:-4] + "\"."))



# ------------------------------------------------------------
# Run the bot, when all things have been set up
# ------------------------------------------------------------
bot.run(token)
