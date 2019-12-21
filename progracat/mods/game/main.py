import discord
from discord.ext import commands

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

def setup(bot):
    bot.add_cog(Game(bot))