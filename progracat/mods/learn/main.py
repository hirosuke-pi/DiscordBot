import discord
from discord.ext import commands
 
from mods.learn.learn import *
import datetime
import traceback
import os, sys


def log(data):
    try:
        dt_now = datetime.datetime.now()
        print('['+ str(dt_now) +'] '+ data)
    except Exception as e:
        print('['+ str(dt_now) +'] [-] '+ str(e.args))


class Learning(commands.Cog, name='学習コマンド'):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(pass_context=True)
    async def talk(self, ctx, args=''):
        """ なにかしゃべるぞ！ """
        if args.isalnum() and args.isdecimal():
            if int(args) > 600:
                await ctx.send(ctx.author.mention + ' 600文字以上はしゃべれないぞ...')
            elif int(args) < 30:
                await ctx.channel.send(ctx.author.mention + ' 30文字以下はしゃべれないぞ...')
            else:
                await ctx.send(get_massage(int(args)))
        else:
            await ctx.send(get_massage())
    

    @commands.command(pass_context=True)
    async def comp(self, ctx, args=''):
        """ 言語データを再コンパイルするぞ！ """
        state = 1
        if args.isalnum() and args.isdecimal():
            if 0 < int(args) < 10:
                state = int(args)

        try:
            compile_text(state)
            await ctx.send(ctx.author.mention + ' 言語データを再コンパイルしたぞ！')
            log("[*] Languages data recompiled. (state="+ str(state) +")")
        except Exception as e:
            await ctx.send(ctx.author.mention + ' コンパイル失敗したぞ...: '+ str(e.args))
            log('[-] Error: ')
            traceback.print_exc()



def setup(bot):
    bot.add_cog(Learning(bot))