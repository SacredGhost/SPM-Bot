import discord
import asyncio
from discord.ext import commands
from SPMDictionary.enemylist import EnemyList
from SPMDictionary.bighexlist import HexList

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

@bot.command(name="enemy")
async def enemy(ctx: commands.Context, *, search: str = ''):
    print('Enemy command executed')

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
    
    search_query = search.strip()
    
    specific_entry = search_enemy_by_name_or_card_num(search_query)
    
    if specific_entry != None:
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
        print(f"EnemyDrops: {specific_entry.EnemyDrops}")
        print(f"DropPercentage: {specific_entry.DropPercent}")
        
        # Check if there are any drops
        if specific_entry.EnemyDrops:
            # Generate drop_info only if there are drops
            drop_info = "\n".join([f"{drop.ItemName}\nItem ID: 0x{drop.ItemID:03X}\nItem Weight: {drop.ItemWeight}" for drop in specific_entry.EnemyDrops if drop.ItemName])
        else:
            drop_info = "No drops for this enemy."
            
        embed = discord.Embed(title=f"Enemy Info: {specific_entry.EnemyName}", color=0x00FF00)
        embed = discord.Embed(title=f"{specific_entry.EnemyName}", description=f"HP: {specific_entry.EnemyData.HP} | Attack: {specific_entry.EnemyData.Atk} | Defence: {specific_entry.EnemyData.Def}", color=0xDB8773) #0xDB8773
        embed.set_thumbnail(url=specific_entry.EnemyData.icon)
        if specific_entry.EnemyData.CardData:
            embed.add_field(name="Card Number", value=specific_entry.EnemyData.CardData.CardNum, inline=True)
            embed.add_field(name="Description", value=specific_entry.EnemyData.CardData.Description, inline=False)
            embed.add_field(name="Tattle", value=specific_entry.EnemyData.Tattle, inline=True)
        else:
            embed.add_field(name="CardData", value="Not available for this enemy.", inline=False)
            embed.add_field(name="Tattle", value=('"', specific_entry.EnemyData.Tattle,'"'), inline=False)
        embed.add_field(name="Enemy Hex", value=f"0x{specific_entry.EnemyID:03X}", inline=False)
        if specific_entry.EnemyDrops and any(drop.ItemName for drop in specific_entry.EnemyDrops):
            # Generate drop_info only if there are drops with non-empty names
            drop_info = "\n".join([f"{drop.ItemName}, {drop.ItemWeight}" for drop in specific_entry.EnemyDrops if drop.ItemName])
        else:
            drop_info = "No drops for this enemy."
        embed.add_field(name="Enemy Drops + Weight", value=drop_info, inline=True)
        ConvertedDropPercent = specific_entry.DropPercent * 100
        print(ConvertedDropPercent)
        embed.add_field(name="Drop Percentage", value=f"{int(ConvertedDropPercent)}%", inline=True)
        
        await ctx.send(embed=embed)
    else:
        print(f"Entry not found for query: {search_query}")
        await ctx.send("Enemy not found in EnemyList.")

@bot.command(name="item")
async def enemy(ctx: commands.Context, *, search: str = ''):
    print('Item command executed')

    def search_item_by_name_or_hex_num(query):
        for item_entry in HexList.values():
            if item_entry.ItemName.lower() == query.lower() or (item_entry.EnemyData.CardData and str(enemy_entry.EnemyData.CardData.CardNum) == query):
                return enemy_entry

        for enemy_entry in EnemyList.values():
            if query.lower() in enemy_entry.EnemyName.lower() or (enemy_entry.EnemyData.CardData and query == str(enemy_entry.EnemyData.CardData.CardNum)):
                return enemy_entry

        return None
    
    search_query = search.strip()
    
    specific_entry = search_item_by_name_or_hex_num(search_query)
    
    if specific_entry != None:
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
        print(f"EnemyDrops: {specific_entry.EnemyDrops}")
        print(f"DropPercentage: {specific_entry.DropPercent}")
        
        # Check if there are any drops
        if specific_entry.EnemyDrops:
            # Generate drop_info only if there are drops
            drop_info = "\n".join([f"{drop.ItemName}\nItem ID: 0x{drop.ItemID:03X}\nItem Weight: {drop.ItemWeight}" for drop in specific_entry.EnemyDrops if drop.ItemName])
        else:
            drop_info = "No drops for this enemy."
            
        embed = discord.Embed(title=f"Enemy Info: {specific_entry.EnemyName}", color=0x00FF00)
        embed = discord.Embed(title=f"{specific_entry.EnemyName}", description=f"HP: {specific_entry.EnemyData.HP} | Attack: {specific_entry.EnemyData.Atk} | Defence: {specific_entry.EnemyData.Def}", color=0xDB8773) #0xDB8773
        embed.set_thumbnail(url=specific_entry.EnemyData.icon)
        if specific_entry.EnemyData.CardData:
            embed.add_field(name="Card Number", value=specific_entry.EnemyData.CardData.CardNum, inline=True)
            embed.add_field(name="Description", value=specific_entry.EnemyData.CardData.Description, inline=False)
            embed.add_field(name="Tattle", value=specific_entry.EnemyData.Tattle, inline=True)
        else:
            embed.add_field(name="CardData", value="Not available for this enemy.", inline=False)
            embed.add_field(name="Tattle", value=('"', specific_entry.EnemyData.Tattle,'"'), inline=False)
        embed.add_field(name="Enemy Hex", value=f"0x{specific_entry.EnemyID:03X}", inline=False)
        if specific_entry.EnemyDrops and any(drop.ItemName for drop in specific_entry.EnemyDrops):
            # Generate drop_info only if there are drops with non-empty names
            drop_info = "\n".join([f"{drop.ItemName}, {drop.ItemWeight}" for drop in specific_entry.EnemyDrops if drop.ItemName])
        else:
            drop_info = "No drops for this enemy."
        embed.add_field(name="Enemy Drops + Weight", value=drop_info, inline=True)
        ConvertedDropPercent = specific_entry.DropPercent * 100
        print(ConvertedDropPercent)
        embed.add_field(name="Drop Percentage", value=f"{int(ConvertedDropPercent)}%", inline=True)
        
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