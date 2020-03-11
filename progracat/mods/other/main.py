import discord
from discord.ext import commands

from mods.learn.learn import *
import datetime
import traceback
import os, sys
import socket


class OtherFunctions(commands.Cog, name='その他コマンド'):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def ping(self, ctx):
        """ 応答時間確認するぞ！ """
        await ctx.send(ctx.author.mention + ' 応答時間は'+ str(round(self.bot.latency * 1000)) +'msだぞ！')
    

    @commands.command(aliases=['y'])
    async def youtube(self, ctx, msg):
        """ クッキー回避版Youtubeリンクに変換するぞ！ """
        video_id = ''
        if msg.find('youtube.com') != -1 or msg.find('youtu.be') != -1:
            video_id_sp = msg.split('=')
            if len(video_id_sp) == 2:
                video_id = video_id_sp[1]
            else:
                video_id_sp = msg.split('/')
                if len(video_id_sp) == 4:
                    video_id = video_id_sp[3]

        if video_id == '':
            await ctx.send(ctx.author.mention + ' リンク変換できなかったぞ...')
        else:
            await ctx.send(ctx.author.mention + ' https://www.youtube-nocookie.com/embed/'+ video_id)

    """
    メッセージを受信したときのイベント
    """
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: # Botによる反応は除外
            return
        
        if message.content.find('完全に理解した') != -1:
            await message.add_reaction('🤔')

        elif message.content.find('炎上') != -1 or message.content.find('爆破') != -1:
            await message.add_reaction('🔥')
    
        elif message.content.find('ハゲ') != -1:
            await message.channel.send(message.author.mention + 'また髪の話してる...(´･ω･`)')

        elif message.content.find('ネコ') != -1:
            await message.add_reaction('😼')

        elif message.content.find('眠い') != -1:
            await message.add_reaction('😪')

        elif message.content.find('社畜') != -1:
            await message.add_reaction('😇')
        
        elif message.content.find('バグ') != -1:
            await message.add_reaction('🐞')

        elif message.content.find('草') != -1:
            await message.add_reaction('🌿')

        elif message.content.find('スパゲッティコード') != -1 or message.content.find('スパゲティーコード') != -1 or message.content.find('スパゲッティーコード') != -1:
            await message.add_reaction('😨')

        elif message.content.find('プログラキャット') != -1 or message.content.find('progracat') != -1:
            await message.channel.send(message.author.mention + '(=^. .^=)ﾐｬｰ')
    
        elif message.content.find('尊い') != -1:
            await message.add_reaction('☺️')
        
        elif message.content.find('ヨシ！') != -1:
            await message.add_reaction('👈')
    
        elif message.content.find('おめ！') != -1 or message.content.find('おめでとう') != -1:
            await message.add_reaction('🥳')

        elif message.content == 'ぬるぽ':
            await message.channel.send(message.author.mention +'■━⊂( ･∀･) 彡 ｶﾞｯ☆`Д´)ﾉ')
        
        elif message.content == 'むりぽ' or message.content == '無理ぽ' or message.content == 'むりぽよ'  or message.content == '無理ぽよ':
            await message.channel.send(message.author.mention +'ヾ(・ω・*)なでなで')
    
        elif message.content == '何かしゃべって' or message.content == 'なんかしゃべって' or message.content == 'なにかしゃべって':
            await message.channel.send(message.author.mention + get_massage())

        else:
            txt_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/learn/text'
            with open(txt_dir + '/discord.txt', 'a', encoding='utf-8') as f:
                f.write('\n' + message.content)

def setup(bot):
    bot.add_cog(OtherFunctions(bot))