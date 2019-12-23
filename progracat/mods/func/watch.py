import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio

import datetime
import random
import traceback
import os, sys


class Watch(commands.Cog, name='時計コマンド'):

    def __init__(self, bot):
        self.bot = bot
        self.stopwatch_dt = None
        self.stopwatch_color = None

    @commands.command(aliases=['w'])
    async def watch(self, ctx):
        """ 今の時間を言うぞ！ """
        dt_now = datetime.datetime.now()
        await ctx.send(ctx.author.mention +'  **' + dt_now.strftime('%Y/%m/%d %H:%M:%S') + '**')

    @commands.command(aliases=['sw'])
    async def stopwatch(self, ctx):
        """ 時間を計測するぞ！ """
        self.stopwatch_dt = datetime.datetime.now()
        self.stopwatch_color = random.randint(0, 0xffffff)

        embed = discord.Embed(title='ストップウォッチを開始したぞ！', color=self.stopwatch_color)
        embed.add_field(name='設定した人', value=ctx.author.mention, inline=True)
        embed.add_field(name='開始時間', value=self.stopwatch_dt.strftime('%Y/%m/%d %H:%M:%S'), inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=['n'])
    async def now(self, ctx):
        """ 今のストップウォッチの経過時間を言うぞ！ """
        if self.stopwatch_dt:
            now_dt = datetime.datetime.now()
            diff = now_dt - self.stopwatch_dt

            embed = discord.Embed(title='ストップウォッチ', color=self.stopwatch_color)
            embed.add_field(name='経過時間', value='**' + str(diff) + '**', inline=True)
            embed.add_field(name='開始時間', value=self.stopwatch_dt.strftime('%Y/%m/%d %H:%M:%S'), inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(ctx.author.mention + ' ストップウォッチが起動してないぞ！')
            

def setup(bot):
    bot.add_cog(Watch(bot))