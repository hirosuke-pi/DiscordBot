import discord
from discord.ext import commands

import datetime
import traceback
import os, sys
import urllib.request
import json
import random
import pokebase as pb


class ProgressBar:

    def __init__(self, max_val):
        self.max = max_val
        self.value = 0
        self.text = 'Pokemon'
    
    def next(self):
        _progress = '['+ self.text[0:self.value] + '=' * (self.max - self.value) +']'
        self.value += 1
        return _progress


class Pokemon(commands.Cog, name='ポケモンコマンド'):

    def __init__(self, bot):
        self.bot = bot
    

    async def send_progress(self, msg, main_msg, pr):
        await msg.edit(content=main_msg+' ' + pr.next())
    

    @commands.command(aliases=['p', 'pokemon'])
    async def poke(self, ctx, msg):
        """ ポケモン図鑑を調べるぞ！サン・ムーンまで対応してるぞ！ """
        load_msg = ctx.author.mention +' 検索中だぞ！ちょっと待ってて...: '
        embed = discord.Embed(title='ポケモン図鑑', color=random.randint(0, 0xffffff))
        await self.pokemon_search(ctx, msg, load_msg, embed)


    @commands.command(aliases=['pk', 'pokemonkuji'])
    async def pokekuji(self, ctx):
        """ ポケモンくじが引けるぞ！ """
        load_msg = ctx.author.mention +' 今くじを引いてるぞ！ちょっと待ってて...: '
        await self.pokemon_search(ctx, random.randint(1, 807), load_msg)


    async def pokemon_search(self, ctx, poke_ser, load_msg, embed=''):
        pr = ProgressBar(7)
        pic_list = ['https://thumbs.gfycat.com/FairSinfulCottontail-small.gif',
                    'https://media.giphy.com/media/3M8bGcZOexuvneoJZl/giphy.gif',
                    'https://cdn.dribbble.com/users/621155/screenshots/2835329/coorzzz.gif',
                    'https://a.top4top.io/p_1990j031.gif',
                    'https://i.pinimg.com/originals/72/00/28/720028e1fce6412e77667993ead54ede.gif',
                    'https://i.pinimg.com/originals/51/72/56/517256bf41fd027b5eec4a38c5110420.gif',
                    'https://media2.giphy.com/media/uXnif9JVu6VnW/source.gif']
        
        type_dict = { 'normal' : 'ノーマル', 'fire' : 'ほのお', 'water' : 'みず', 'grass' : 'くさ', 'electic' : 'でんき',
                      'ice' : 'こおり', 'fighting' : 'かくとう', 'poison' : 'どく', 'ground' : 'じめん', 'flying' : 'ひこう',
                      'psychic' : 'エスパー', 'bug' : 'むし', 'rock' : 'いわ', 'ghost' : 'ゴースト', 'dragon' : 'ドラゴン',
                      'dark' : 'あく', 'steel' : 'はがね', 'fairy' : 'フェアリー' }
        
        type_list = ['ノーマル', 'ほのお', 'みず', 'くさ', 'でんき',
                     'こおり', 'かくとう', 'どく', 'じめん', 'ひこう',
                     'エスパー', 'むし', 'いわ', 'ゴースト', 'ドラゴン',
                     'あく', 'はがね', 'フェアリー']

        tmp = await ctx.send(load_msg)
        load_pic = discord.Embed(title='', description='', color=random.randint(0, 0xffffff))
        load_pic.set_image(url=random.choice(pic_list))
        load_pic_msg = await ctx.send(embed=load_pic)

        try:
            await self.send_progress(tmp, load_msg, pr)
        
            sp_data = pb.pokemon_species(poke_ser)
            await self.send_progress(tmp, load_msg, pr)
            p_data = pb.pokemon(poke_ser)
            await self.send_progress(tmp, load_msg, pr)

            weight = float(p_data.weight) / 10
            poke_num = sp_data.id
            name_en = sp_data.name

            type_names = []
            for t in p_data.types:
                type_names.append(type_list[t.slot])
            type_name = ', '.join(type_names)
            await self.send_progress(tmp, load_msg, pr)

            stats_dict = {}
            for s in p_data.stats:
                stats_dict[s.stat.name] = s.base_stat
            await self.send_progress(tmp, load_msg, pr)

            flavor = ''
            for data in sp_data.flavor_text_entries:
                if data.language.name.find('ja') != -1:
                    flavor = data.flavor_text
                    break
            await self.send_progress(tmp, load_msg, pr)

            name = ''
            for data in sp_data.names:
                if data.language.name.find('ja') != -1:
                    name = data.name
                    break
            await self.send_progress(tmp, load_msg, pr)

            genus = ''
            for data in sp_data.genera:
                if data.language.name.find('ja') != -1:
                    genus = data.genus
                    break
            await self.send_progress(tmp, load_msg, pr)

            seed_sum = stats_dict['hp'] + stats_dict['attack'] + stats_dict['special-attack'] + stats_dict['special-defense'] + stats_dict['defense'] + stats_dict['speed']

            if embed == '':
                embed = discord.Embed(title='ポケモンくじ', description='今日の'+ ctx.author.mention + 'のラッキーポケモンは... '+ name +'！', color=random.randint(0, 0xffffff))
            embed.add_field(name='図鑑番号', value=str(poke_num), inline=True)
            embed.add_field(name='名前', value=name + ' ('+ name_en +')', inline=True)
            embed.add_field(name='分類', value=genus, inline=True)
            embed.add_field(name='タイプ', value=type_name, inline=True)
            embed.set_image(url='https://raw.githubusercontent.com/fanzeyi/pokemon.json/master/images/'+ str(poke_num).zfill(3) +'.png')
            embed.add_field(name='体力', value=str(stats_dict['hp']), inline=True)
            embed.add_field(name='攻撃力', value=str(stats_dict['attack']), inline=True)
            embed.add_field(name='特攻', value=str(stats_dict['special-attack']), inline=True)
            embed.add_field(name='防御力', value=str(stats_dict['defense']), inline=True)
            embed.add_field(name='特防', value=str(stats_dict['special-defense']), inline=True)
            embed.add_field(name='速度', value=str(stats_dict['speed']), inline=True)
            embed.add_field(name='種族値合計', value=str(seed_sum), inline=True)
            embed.add_field(name='重さ', value=str(weight) +'kg', inline=True)
            embed.add_field(name='説明', value=flavor, inline=False)
        
            await tmp.delete()
            await load_pic_msg.delete()
            await ctx.send(embed=embed)

        except ValueError as e:
            await tmp.edit(content=ctx.author.mention + ' '+ poke_ser +'は見つからなかったぞ...')
        except Exception as e:
            await tmp.edit(content=ctx.author.mention + ' エラーだぞ！: '+ str(e.args))

        

def setup(bot):
    bot.add_cog(Pokemon(bot))