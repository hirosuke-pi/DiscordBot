import discord
from discord.ext import commands
import asyncio

import random
import datetime
import traceback
import os, sys


class Game(commands.Cog, name='一息ゲームコマンド'):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def mine(self, ctx):
        """ 14x14のマインスイーパを生成するぞ！ """
        bomb_list = []
        num_dict = { 0 : '0⃣', 1 : '1⃣', 2 : '2⃣', 3 : '3⃣', 4 : '4⃣', 5 : '5⃣', 6 : '6⃣', 7 : '7⃣', 8 : '8⃣', 9 : '9⃣'}
        search_list = ((-1, -1), (0, -1), (1, -1),
                       (-1, 0),           (1, 0),  
                       (-1, 1),  (0, 1),  (1, 1))
        X = 14
        Y = 14

        # ボム生成
        for y in range(Y):
            bomb_list.append([9 if random.randint(0, 15) == 1 else 0 for i in range(X)])
        
        # ボム位置の把握
        for y in range(Y):
            for x in range(X):
                count = 0
                if bomb_list[y][x] != 9:
                    for s_ptr in search_list:
                        tmp_x = x + s_ptr[0]
                        tmp_y = y + s_ptr[1]
                        if 0 <= tmp_x < X and 0 <= tmp_y < Y:
                            if bomb_list[tmp_y][tmp_x] == 9:
                                count += 1
                    bomb_list[y][x] = count

        # 文字列に変換
        mine_data = ''
        for bomb_ptr in bomb_list:
            #print(bomb_ptr)
            for bomb in bomb_ptr:
                if bomb == 9:
                    mine_data += '||#⃣||'
                else:
                    mine_data += '||'+ num_dict[bomb] + '||'
            mine_data += '\r\n'
        await ctx.send(mine_data)
            

    @commands.command()
    async def slot(self, ctx):
        """スロットを回すぞ！"""
        def make_slot_txt(s):
            txt = '**'
            for i in range(0, 3):
                txt += '['+ s[i][0] +'] ['+ s[i][1] +'] ['+ s[i][2] +']\r\n'
            return txt + '**'

        def set_slot(s, item, x):
            r = random.randint(0, 8)
            for i in range(0, 3):
                s[i][x] = item[r]
                r += 1
                if r > 8: r = 0
            return s

        s = [['㊙️', '㊙️', '㊙️'], ['㊙️', '㊙️', '㊙️'], ['㊙️', '㊙️', '㊙️']]
        item = ['7⃣', '🔔', '🍉', '🍌', '🍋', '🍊', '🍒', '🍇', '🎰']
        num = { '0⃣' : 0, '1⃣' : 1, '2⃣' : 2 }

        slot_txt = await ctx.send(make_slot_txt(s))

        await slot_txt.add_reaction('0⃣')
        await slot_txt.add_reaction('1⃣')
        await slot_txt.add_reaction('2⃣')

        def check(reaction, user):
            emoji = str(reaction.emoji)
            if user.bot == True:    # botは無視
                pass
            else:
                return emoji == '0⃣' or emoji == '1⃣' or emoji == '2⃣' or emoji == '🔄'

        cnt = 0
        index_list = []
        while not self.bot.is_closed():
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
            except asyncio.TimeoutError:
                await slot_txt.add_reaction('😪')
                break
            else:
                if ctx.author.id != user.id:
                    continue
                if str(reaction.emoji) == '🔄' and cnt >= 3:
                    index_list = list()
                    cnt = 0
                    s = [['㊙️', '㊙️', '㊙️'], ['㊙️', '㊙️', '㊙️'], ['㊙️', '㊙️', '㊙️']]
                    await slot_txt.edit(content=make_slot_txt(s))
                    continue

                cnt += 1
                index = num[str(reaction.emoji)]

                if index not in index_list:
                    index_list.append(index)
                    s = set_slot(s, item, index)
                    await slot_txt.edit(content=make_slot_txt(s))
                    if cnt >= 3: 
                        await slot_txt.add_reaction('🔄')

    

def setup(bot):
    bot.add_cog(Game(bot))