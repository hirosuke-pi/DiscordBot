import discord
from discord.ext import commands

import datetime
import traceback
import os, sys
import urllib.request
import json
import random
import pokebase as pb
import traceback
import math


class ProgressBar:

    def __init__(self, max_val):
        self.max = max_val
        self.value = 0
        self.text = 'Pokemon!'
    
    def next(self):
        _progress = '['+ self.text[0:self.value] + '=' * (self.max - self.value) +']'
        self.value += 1
        return _progress


class PokemonValues:

    def __init__(self):
        self.level = random.randint(1, 100)
        self.gender = 'なし'
        self.__set_per()
        self.indi_judge_dict = {}
        self.indi_dict = {
            'hp'              : random.randint(0, 31),
            'attack'          : random.randint(0, 31),
            'defense'         : random.randint(0, 31),
            'special-attack'  : random.randint(0, 31),
            'special-defense' : random.randint(0, 31),
            'speed'           : random.randint(0, 31)
        }

        for k, v in self.indi_dict.items():
            self.indi_judge_dict[k] = self.__judge_poke_indi(v)

        self.indi_sum = sum(self.indi_dict.values())
        self.indi_sum_judge = self.__judge_poke_indi_sum(self.indi_sum)

        self.seed_dict = {
            'hp'              : 0,
            'attack'          : 0,
            'defense'         : 0,
            'special-attack'  : 0,
            'special-defense' : 0,
            'speed'           : 0
        }

        self.effort_dict = {
            'hp'              : 0,
            'attack'          : 0,
            'defense'         : 0,
            'special-attack'  : 0,
            'special-defense' : 0,
            'speed'           : 0
        }

        self.abilities = {
            'hp'              : 0,
            'attack'          : 0,
            'defense'         : 0,
            'special-attack'  : 0,
            'special-defense' : 0,
            'speed'           : 0
        }

        self.state_abi = {
            'attack'          : 0,
            'defense'         : 1,
            'special-attack'  : 2,
            'special-defense' : 3,
            'speed'           : 4
        }

        self.state_indi = {
            'hp'              : 0,
            'attack'          : 1,
            'defense'         : 2,
            'special-attack'  : 3,
            'special-defense' : 4,
            'speed'           : 5
        }

        self.abi_jp = {
            'hp'              : 'たいりょく',
            'attack'          : 'こうげき',
            'defense'         : 'ぼうぎょ',
            'special-attack'  : 'とくこう',
            'special-defense' : 'とくぼう',
            'speed'           : 'すばやさ'
        }

        self.id = 0
        self.name = ''
        self.name_en = ''
        self.type = ''
        self.weight = 0
        self.height = 0
        self.flavor = ''
        self.genus = ''
        self.ability_name = ''
        self.img_id = ''

    
    def __judge_poke_indi_sum(self, val):
        seed_sum_list = ['素晴らしい能力！', '相当優秀な能力', '平均以上の能力', 'まずまずの能力']
        if 151 <= val <= 186:
            return seed_sum_list[0]
        elif 121 <= val <= 150:
            return seed_sum_list[1]
        elif 91 <= val <= 120:
            return seed_sum_list[2]
        elif 0 <= val <= 90:
            return seed_sum_list[3]

    
    def __judge_poke_indi(self, val):
        seed_list = ['さいこう', 'すばらしい', 'すごくいい', 'かなりいい', 'まあまあ', 'ダメかも']
        if val == 31:
            return seed_list[0]
        elif val == 30:
            return seed_list[1]
        elif 26 <= val <= 29:
            return seed_list[2]
        elif 16 <= val <= 25:
            return seed_list[3]
        elif 1 <= val <= 15:
            return seed_list[4]
        else:
            return seed_list[5]

    
    def __set_per(self):
        personality = ['さみしがり', 'いじっぱり', 'やんちゃ', 'ゆうかん', 'ずぶとい', 'わんぱく', 'のうてんき',
                       'のんき', 'ひかえめ', 'おっとり', 'うっかりや', 'れいせい', 'おだやか', 'おとなしい', 'しんちょう',
                       'なまいき', 'おくびょう', 'せっかち', 'ようき', 'むじゃき', 'てれや', 'すなお', 'まじめ', 'きまぐれ', 'がんばりや']
        self.per_value = random.randint(0, len(personality) - 1)
        self.personality = personality[self.per_value]


    def set_gender(self, value):
        if value == -1:
            self.gender = 'なし'
        elif value == 0:
            self.gender = 'オス♂'
        elif value == 8:
            self.gender = 'メス♀'
        else:
            self.gender = random.choice(['オス♂', 'メス♀'])
    

    def set_type(self, type_list):
        type_dict = { 'normal' : 'ノーマル', 'fire' : 'ほのお', 'water' : 'みず', 'grass' : 'くさ', 'electric' : 'でんき',
                      'ice' : 'こおり', 'fighting' : 'かくとう', 'poison' : 'どく', 'ground' : 'じめん', 'flying' : 'ひこう',
                      'psychic' : 'エスパー', 'bug' : 'むし', 'rock' : 'いわ', 'ghost' : 'ゴースト', 'dragon' : 'ドラゴン',
                      'dark' : 'あく', 'steel' : 'はがね', 'fairy' : 'フェアリー' }
        tmp_list = []
        for type_ in type_list:
            tmp_list.append(type_dict[type_])
        
        self.type = ','.join(tmp_list)
    

    def set_level(self, min_lv):
        if min_lv != None:
            self.level = random.randint(min_lv, 100)
    

    def __calc_hp(self, seed_val, indi_val, effort_val, lv):
        return math.floor((((seed_val * 2) + indi_val + (effort_val / 4)) * (lv / 100)) + (lv + 10))
    
    def __calc_ability(self, seed_val, indi_val, effort_val, lv, pri_val, abi_val):
        ptr_list = [
            [1, -1, 0, 0, 0],
            [1, 0, -1, 0, 0],
            [1, 0, 0, -1, 0],
            [1, 0, 0, 0, -1],
            [-1, 1, 0, 0, 0],
            [0, 1, -1, 0, 0],
            [0, 1, 0, -1, 0],
            [0, 1, 0, 0, -1],
            [-1, 0, 1, 0, 0],
            [0, -1, 1, 0, 0],
            [0, 0, 1, -1, 0],
            [0, 0, 1, 0, -1],
            [-1, 0, 0, 1, 0],
            [0, -1, 0, 1, 0],
            [0, 0, -1, 1, 0],
            [0, 0, 0, 1, -1],
            [-1, 0, 0, 0, 1],
            [0, -1, 0, 0, 1],
            [0, 0, -1, 0, 1],
            [0, 0, 0, -1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        ptr = ptr_list[pri_val][abi_val]

        if ptr == 1:
            comp = 1.1
        elif ptr == -1:
            comp = 0.9
        else:
            comp = 1.0
        
        return math.floor(((((seed_val * 2) + indi_val + (effort_val / 4)) * (lv / 100)) + 5) * comp)
    

    def calc(self):
        if self.id == 662:
            self.img_id = '662r'
        elif self.id == 740:
            self.img_id = '740re'
        else:
            self.img_id = str(self.id).zfill(3)

        self.seed_sum = sum(self.seed_dict.values())
        for k in self.abilities.keys():
            if k == 'hp':
                self.abilities[k] = self.__calc_hp(self.seed_dict[k], self.indi_dict[k], self.effort_dict[k], self.level)
            else:
                self.abilities[k] = self.__calc_ability(self.seed_dict[k], self.indi_dict[k], self.effort_dict[k], self.level, self.per_value, self.state_abi[k])



class Pokemon(commands.Cog, name='ポケモンコマンド'):

    def __init__(self, bot):
        self.bot = bot
    

    async def send_progress(self, msg, main_msg, pr):
        await msg.edit(content=main_msg+' ' + pr.next())


    def embed_poke_catch(self, embed, pv):
        for k, v in pv.abi_jp.items():
            ab_val = pv.indi_dict[k]
            embed.add_field(name=v, value='```' + str(pv.abilities[k]).ljust(3, ' ') + ' ['+ ('=' * ab_val) + ('.' * (31 - ab_val)) +']' +'``` '+ pv.indi_judge_dict[k]+'', inline=False)
    

    def embed_poke_pic(self, embed, pv):
        for k, v in pv.abi_jp.items():
            embed.add_field(name=v, value='```' + str(pv.seed_dict[k]) +'```', inline=True)
    

    def get_risk(self):
        risk_list = [True for _ in range(0, 20)]
        risk_list.append(False)
        random.shuffle(risk_list)
        return random.choice(risk_list)


    @commands.command(aliases=['p', 'pokemon'])
    async def poke(self, ctx, msg):
        """ ポケモン図鑑を調べるぞ！サン・ムーンまで対応してるぞ！ """
        load_msg = ctx.author.mention +' 検索中だぞ！ちょっと待ってて...: '
        embed = discord.Embed(title='ポケモン図鑑', color=random.randint(0, 0xffffff))
        await self.pokemon_search(ctx, msg, load_msg, False, embed)


    @commands.command(aliases=['pc', 'catch'])
    async def pokecatch(self, ctx):
        """ ポケモンを捕まえるぞ！ """
        load_msg = ctx.author.mention +'はモンスターボールを投げた！ 結果は...: '
        print('cmd')
        try:
            await self.pokemon_search(ctx, random.randint(1, 807), load_msg, True)
        except:
            traceback.print_exc()


    async def pokemon_search(self, ctx, poke_ser, load_msg, flag, embed=''):
        pr = ProgressBar(8)
        pv = PokemonValues()
        print('pokemon_id: '+ str(poke_ser))

        pic_list = ['https://thumbs.gfycat.com/FairSinfulCottontail-small.gif',
                    'https://media.giphy.com/media/3M8bGcZOexuvneoJZl/giphy.gif',
                    'https://cdn.dribbble.com/users/621155/screenshots/2835329/coorzzz.gif',
                    'https://a.top4top.io/p_1990j031.gif',
                    'https://i.pinimg.com/originals/72/00/28/720028e1fce6412e77667993ead54ede.gif',
                    'https://i.pinimg.com/originals/51/72/56/517256bf41fd027b5eec4a38c5110420.gif',
                    'https://media2.giphy.com/media/uXnif9JVu6VnW/source.gif']

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

            pv.weight = float(p_data.weight) / 10
            pv.height = float(p_data.height) / 10
            pv.id = sp_data.id
            pv.name_en = sp_data.name
            pv.set_gender(sp_data.gender_rate)

            evo_chain_id = int(sp_data.evolution_chain.url.split('/')[6])

            type_names = []
            for t in p_data.types:
                type_names.append(t.type.name)
            pv.set_type(type_names)
            await self.send_progress(tmp, load_msg, pr)

            for s in p_data.stats:
                pv.seed_dict[s.stat.name] = s.base_stat
            await self.send_progress(tmp, load_msg, pr)

            for data in sp_data.flavor_text_entries:
                if data.language.name.find('ja') != -1:
                    pv.flavor = data.flavor_text
                    break
            await self.send_progress(tmp, load_msg, pr)

            for data in sp_data.names:
                if data.language.name.find('ja') != -1:
                    pv.name = data.name
                    break
            await self.send_progress(tmp, load_msg, pr)

            for data in sp_data.genera:
                if data.language.name.find('ja') != -1:
                    pv.genus = data.genus
                    break
            await self.send_progress(tmp, load_msg, pr)

            try:
                evo = pb.evolution_chain(evo_chain_id)
                min_lv = evo.chain.evolves_to[0]['evolution_details'][0]['min_level']
                #print(min_lv)
                pv.set_level(min_lv)
            except:
                #traceback.print_exc()
                pv.set_level(30)

            abi_id = random.choice(p_data.abilities).ability.url.split('/')[6]
            for data in pb.ability(abi_id).names:
                if data.language.name.find('ja') != -1:
                    pv.ability_name = data.name
                    break

            pv.calc()
            await self.send_progress(tmp, load_msg, pr)

            print('indi_sum: ' + str(pv.indi_dict))
            #print('seed_dict: '+ str(pv.seed_dict))

            if embed == '':
                embed = discord.Embed(title='ポケモンをつかまえた！', description=ctx.author.mention + 'は、'+ pv.name +'をつかまえた！', color=random.randint(0, 0xffffff))
            embed.add_field(name='図鑑番号', value=str(pv.id), inline=True)
            embed.add_field(name='名前', value=pv.name + ' ('+ pv.name_en +')', inline=True)
            embed.add_field(name='分類', value=pv.genus, inline=True)
            embed.add_field(name='タイプ', value=pv.type, inline=True)
            if flag: 
                embed.add_field(name='せいべつ', value=str(pv.gender), inline=True)
                embed.add_field(name='レベル', value='```' + str(pv.level) + '```', inline=True)
            embed.set_image(url='https://raw.githubusercontent.com/fanzeyi/pokemon.json/master/images/'+ pv.img_id +'.png')
            if flag:
                self.embed_poke_catch(embed, pv)
            else:
                self.embed_poke_pic(embed, pv)
            embed.add_field(name='種族値合計', value='```' + str(pv.seed_sum) + '```', inline=True)
            if flag: 
                embed.add_field(name='個体値', value=pv.indi_sum_judge, inline=True)
                embed.add_field(name='せいかく', value=pv.personality, inline=True)
            embed.add_field(name='とくせい', value=pv.ability_name, inline=True)
            embed.add_field(name='おもさ', value=str(pv.weight) +'kg', inline=True)
            embed.add_field(name='たかさ', value=str(pv.height)+'m', inline=True)
            embed.add_field(name='説明', value=pv.flavor, inline=False)

            await tmp.delete()
            await load_pic_msg.delete()

            if self.get_risk() or not(flag):
                await ctx.send(embed=embed)
            else:
                await ctx.send(ctx.author.mention + ' 野生の**'+ pv.name +'**は逃げ出した！')

        except ValueError as e:
            await load_pic_msg.delete()
            await tmp.edit(content=ctx.author.mention + ' '+ poke_ser +'は見つからなかったぞ...')
        except Exception as e:
            await load_pic_msg.delete()
            traceback.print_exc()
            await tmp.edit(content=ctx.author.mention + ' エラーだぞ！: '+ str(e.args))

        

def setup(bot):
    bot.add_cog(Pokemon(bot))