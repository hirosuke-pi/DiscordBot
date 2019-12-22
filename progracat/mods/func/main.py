import discord
from discord.ext import commands

import datetime
import traceback
import os, sys
import urllib.request
import json
import random
import pokebase as pb


class Functions(commands.Cog, name='機能コマンド'):

    def __init__(self, bot):
        self.bot = bot
    

    def search_ja(self, p_dict):

        return ''
    
    @commands.command()
    async def pokekuji(self, ctx):
        """ ポケモンくじが引けるぞ！ """

        poke_num = random.randint(1, 809)
        sp_data = pb.pokemon_species(poke_num)
        p_data = pb.pokemon(poke_num)

        weight = float(p_data.weight) / 10

        type_names = []
        for t in p_data.types:
            tp = pb.type_(t.type.name)
            for t_name in tp.names:
                if t_name.language.name.find('ja') != -1:
                    type_names.append(t_name.name)
        type_name = ', '.join(type_names)

        stats_dict = {}
        for s in p_data.stats:
            stats_dict[s.stat.name] = s.base_stat

        flavor = ''
        for data in sp_data.flavor_text_entries:
            if data.language.name.find('ja') != -1:
                flavor = data.flavor_text
        name = ''
        for data in sp_data.names:
            if data.language.name.find('ja') != -1:
                name = data.name
        genus = ''
        for data in sp_data.genera:
            if data.language.name.find('ja') != -1:
                genus = data.genus

        embed = discord.Embed(title='ポケモンくじ', description='今日の'+ ctx.author.mention + 'のラッキーポケモンは... '+ name +'！', color=random.randint(0, 0xffffff))
        embed.add_field(name='図鑑番号', value=str(poke_num), inline=True)
        embed.add_field(name='名前', value=name, inline=True)
        embed.add_field(name='分類', value=genus, inline=True)
        embed.add_field(name='タイプ', value=type_name, inline=True)
        embed.set_image(url='https://raw.githubusercontent.com/fanzeyi/pokemon.json/master/images/'+ str(poke_num).zfill(3) +'.png')
        embed.add_field(name='体力', value=str(stats_dict['hp']), inline=True)
        embed.add_field(name='攻撃力', value=str(stats_dict['attack']), inline=True)
        embed.add_field(name='防御力', value=str(stats_dict['defense']), inline=True)
        embed.add_field(name='速度', value=str(stats_dict['speed']), inline=True)
        embed.add_field(name='重さ', value=str(weight) +'kg', inline=True)
        embed.add_field(name='説明', value=flavor, inline=False)
        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Functions(bot))