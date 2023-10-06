import discord
import asyncio
from discord.ext import commands
from SPMDictionary.enemylist import EnemyList

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
  print('SPM-Bot is awake | {0.user}'.format(client))
  await bot.change_presence(status=discord.Status.online, activity=discord.Game('Super Paper Mario')) 

def search_enemy_by_name_or_card_num(query):
    # First, try to find an exact match by name or card number
    for enemy_entry in EnemyList.values():
        if enemy_entry.EnemyName.lower() == query.lower() or (enemy_entry.EnemyData.CardData and str(enemy_entry.EnemyData.CardData.CardNum) == query):
            return enemy_entry

    # If no exact match is found, search for partial matches by name or card number
    for enemy_entry in EnemyList.values():
        if query.lower() in enemy_entry.EnemyName.lower() or (enemy_entry.EnemyData.CardData and query == str(enemy_entry.EnemyData.CardData.CardNum)):
            return enemy_entry

    return None

@bot.command(name="enemy")
async def enemy(ctx: commands.Context, *, search: str = ''):
    print('Enemy command executed')
    
    # Remove the command prefix and leading whitespace from the search query
    search_query = search.strip()
    
    specific_entry = search_enemy_by_name_or_card_num(search_query)
    
    if specific_entry is not None:
        print(f"Found entry: {specific_entry.EnemyName}")
        
        # Debugging information
        print(f"EnemyName: {specific_entry.EnemyName}")
        print(f"EnemyHex: {specific_entry.EnemyID}")
        print(f"HP: {specific_entry.EnemyData.HP}")
        print(f"Attack: {specific_entry.EnemyData.Atk}")
        print(f"Defense: {specific_entry.EnemyData.Def}")
        print(f"Icon: {specific_entry.EnemyData.icon}")
        if specific_entry.EnemyData.CardData:
            print(f"CardNumber: {specific_entry.EnemyData.CardData.CardNum}")
            print(f"Description: {specific_entry.EnemyData.CardData.Description}")
        else:
            print("CardData not available for this enemy.")
        print(f"Tattle: {specific_entry.EnemyData.Tattle}")

        # Debugging specific_entry.EnemyDrops
        print(f"EnemyDrops: {specific_entry.EnemyDrops}")
        
        # Check if there are any drops
        if specific_entry.EnemyDrops:
            # Generate drop_info only if there are drops
            drop_info = "\n".join([f"Item Name: {drop.ItemName}\nItem ID: 0x{drop.ItemID:03X}\nItem Weight: {drop.ItemWeight}" for drop in specific_entry.EnemyDrops if drop.ItemName])
        else:
            drop_info = "No drops for this enemy."
            
        # Create the embed as before
        embed = discord.Embed(title=f"Enemy Info: {specific_entry.EnemyName}", color=0x00FF00)
        embed.add_field(name="EnemyHex", value=f"0x{specific_entry.EnemyID:03X}", inline=False)
        embed.add_field(name="HP", value=specific_entry.EnemyData.HP, inline=True)
        embed.add_field(name="Attack", value=specific_entry.EnemyData.Atk, inline=True)
        embed.add_field(name="Defense", value=specific_entry.EnemyData.Def, inline=True)
        embed.add_field(name="Icon", value=specific_entry.EnemyData.icon, inline=False)
        if specific_entry.EnemyData.CardData:
            embed.add_field(name="CardNumber", value=specific_entry.EnemyData.CardData.CardNum, inline=True)
            embed.add_field(name="Description", value=specific_entry.EnemyData.CardData.Description, inline=False)
        else:
            embed.add_field(name="CardData", value="Not available for this enemy.", inline=False)
        embed.add_field(name="Tattle", value=specific_entry.EnemyData.Tattle, inline=False)
        if specific_entry.EnemyDrops and any(drop.ItemName for drop in specific_entry.EnemyDrops):
            # Generate drop_info only if there are drops with non-empty names
            drop_info = "\n".join([f"Item Name: {drop.ItemName}\nItem ID: 0x{drop.ItemID:03X}\nItem Weight: {drop.ItemWeight}" for drop in specific_entry.EnemyDrops if drop.ItemName])
        else:
            drop_info = "No drops for this enemy."
        embed.add_field(name="Enemy Drops", value=drop_info, inline=False)
        
        # Send the embed
        await ctx.send(embed=embed)
    else:
        print(f"Entry not found for query: {search_query}")
        await ctx.send("Enemy not found in EnemyList.")

file_path = 'C:\keys.txt'
with open(file_path, 'r') as file:
    file_content = file.read()

async def main():
    await bot.start(file_content)

asyncio.run(main())