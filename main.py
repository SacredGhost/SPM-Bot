import discord
import os
import asyncio
from discord.ext import commands

import sys
print(sys.version)

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

prefix = '?'
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.command()
async def ping(ctx):
  await ctx.reply(f"{round(bot.latency * 1000)}ms")

@bot.event
async def on_ready():
  print('SPM Bot is awake | {0.user}'.format(client))
  await bot.change_presence(status=discord.Status.online, activity=discord.Game('Super Paper Mario'))

async def load():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      await bot.load_extension(f'cogs.{filename[:-3]}')

file_path = 'C:\keys.txt'
with open(file_path, 'r') as file:
    file_content = file.read()

async def main():
  await load()
  await bot.start(file_content)

asyncio.run(main())