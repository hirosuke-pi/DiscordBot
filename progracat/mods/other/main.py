import discord
from discord.ext import commands

from mods.learn.learn import *
import datetime
import traceback
import os, sys


class OtherFunctions(commands.Cog, name='その他コマンド'):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ver(self, ctx):
        """ バージョン確認するぞ！ """
        await ctx.send(ctx.author.mention + ' バージョンは'+ __version__ +'だぞ！')

    """
    メッセージを受信したときのイベント
    """
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: # Botによる反応は除外
            return
        
        if message.content.find('完全に理解した') != -1:
            await message.add_reaction('🤔')

        elif message.content.find('炎上') != -1:
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
    
        elif message.content.find('おめ！') != -1 or message.content.find('おめでとう') != -1:
            await message.add_reaction('🥳')

        elif message.content == 'ぬるぽ':
            await message.channel.send(message.author.mention +'■━⊂( ･∀･) 彡 ｶﾞｯ☆`Д´)ﾉ')
    
        elif message.content == '何かしゃべって' or message.content == 'なんかしゃべって' or message.content == 'なにかしゃべって':
            await message.channel.send(message.author.mention + get_massage())

        else:
            txt_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/learn/text'
            with open(txt_dir + '/discord.txt', 'a', encoding='utf-8') as f:
                f.write('\n' + message.content)

def setup(bot):
    bot.add_cog(OtherFunctions(bot))