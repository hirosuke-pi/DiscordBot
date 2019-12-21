from discord.ext import commands
import discord

import traceback
import os, sys
import subprocess
import threading
import time
import datetime


def log(data):
    try:
        dt_now = datetime.datetime.now()
        print('['+ str(dt_now) +'] '+ data)
    except Exception as e:
        print('['+ str(dt_now) +'] [-] '+ str(e.args))


class ProgramEmu:
    def __init__(self, bot, ctx):
        self.programs = ''  # プログラム内容
        self.launcher = '' # プログラム実行ファイル
        self.fileext = ''  # プログラムファイル拡張子
        self.programs = ''
        self.bot = bot
        self.ctx = ctx


        self.timeout = 30
        self.timedout_flag = False


    def get_filepath(self):
        """ プログラムファイル名取得 """
        if os.name == 'nt':
            return os.path.dirname(os.path.abspath(__file__)) + '\\index.' + self.fileext
        else:
            return os.path.dirname(os.path.abspath(__file__))+ '/index.' + self.fileext


    def get_mentions(self):
        """ 全員分のメンションを取得 """
        mention_dict = {}
        for member in self.bot.get_all_members():
            mention_dict[member.name] = member.mention
        return mention_dict


    async def compile(self):
        """ プログラムの設定完了 """

        # メンション辞書追加
        if self.fileext == 'py':
            self.programs = '# -*- coding: utf-8 -*-\r\nmentions = ' + str(self.get_mentions()) + '\r\n' + self.programs
        elif self.fileext == 'rb':
            self.programs = 'mentions = ' + str(self.get_mentions()).replace("': '", "' => '") + ';\r\n' + self.programs
        elif self.fileext == 'js':
            self.programs = 'var mentions = ' + str(self.get_mentions()) + '\r\n' + self.programs
        elif self.fileext == 'php':
            self.programs = '<?php\r\n$mentions = array(' + str(self.get_mentions()).replace("': '", "' => '").rstrip('}').lstrip('{') + ');\r\n' + self.programs
        elif self.fileext == 'pl':
            self.programs = 'use strict;\r\nuse warnings;\r\nmy %mentions = (' + str(self.get_mentions()).replace("': '", "' => '").rstrip('}').lstrip('{') + ');\r\n' + self.programs

        try:
            # プログラム書き込み
            with open(self.get_filepath(), 'w', encoding='utf-8') as f:
                f.write(self.programs)
            await self.ctx.message.add_reaction('👌')
            return True
        except:
            log('[-] IO Error:')
            traceback.print_exc()
            await self.ctx.message.add_reaction('😖')
            return False
    

    def moniter_process(self, proc):
        """ プロセス監視 """

        self.timedout_flag = False
        count = 0
        while True:
            count += 1
            time.sleep(1)
            if proc.poll() is not None:
                break
            if count > self.timeout:
                proc.kill()
                self.timedout_flag = True
                break


    async def run(self):
        """ エミュレータ起動 """

        try:
            # プロセス起動
            proc = subprocess.Popen([self.launcher, self.get_filepath()], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # プロセス監視スレッド開始
            th = threading.Thread(target=self.moniter_process, args=(proc, ))
            th.start()
            log('[*] Process started. timeout:'+ str(self.timeout) +'s')

            # 実行データ取得
            output = ''
            try:
                output = proc.stdout.read().decode('utf-8')
            except:
                output = proc.stdout.read().decode('shift-jis')
            
            # 制限時間内に終了しなかったら強制終了
            if self.timedout_flag:
                log('[+] Program timed out. ')
                await self.ctx.message.add_reaction('🥱')
                return ''

            # 実行データ送信
            if output.strip() == '':
                await self.ctx.message.add_reaction('🥴')
                return ''
            log('[+] Program exited. ')

            return output

        except:
            log('[-] Error:')
            traceback.print_exc()
            await self.ctx.message.add_reaction('😖')
            return ''



class ProgrammingEmulator(commands.Cog, name='プログラミング・エミュレーターコマンド'):

    def __init__(self, bot):
        self.bot = bot
        self.timeout = 30
    
    async def run_emulator(self, ctx, emu):
        emu.timeout = self.timeout
        await emu.compile()
        recv_data = await emu.run()
        if recv_data != '':
            await ctx.send(recv_data)

    @commands.command()
    async def py(self, ctx, *, msg):
        """ Pythonのプログラムを実行するぞ！ """
        emu = ProgramEmu(self.bot, ctx)
        emu.launcher = 'python3'
        emu.fileext = 'py'
        emu.programs = msg[4:len(msg)].rstrip('```').lstrip('```python').lstrip('```py')
        await self.run_emulator(ctx, emu)


    @commands.command()
    async def rb(self, ctx, *, msg):
        """ Rubyのプログラムを実行するぞ！ """
        emu = ProgramEmu(self.bot, ctx)
        emu.launcher = 'ruby'
        emu.fileext = 'rb'
        emu.programs = msg[4:len(msg)].rstrip('```').lstrip('```ruby').lstrip('```rb')
        await self.run_emulator(ctx, emu)
    

    @commands.command()
    async def js(self, ctx, *, msg):
        """ JavaScriptのプログラムを実行するぞ！ """
        emu = ProgramEmu(self.bot, ctx)
        emu.launcher = 'node'
        emu.fileext = 'js'
        emu.programs = msg[4:len(msg)].rstrip('```').lstrip('```js')
        await self.run_emulator(ctx, emu)
    

    @commands.command()
    async def php(self, ctx, *, msg):
        """ PHPのプログラムを実行するぞ！ """
        emu = ProgramEmu(self.bot, ctx)
        emu.launcher = 'php'
        emu.fileext = 'php'
        emu.programs = msg[5:len(msg)].rstrip('```').lstrip('```php')
        await self.run_emulator(ctx, emu)


    @commands.command()
    async def perl(self, ctx, *, msg):
        """ Perlのプログラムを実行するぞ！ """
        emu = ProgramEmu(self.bot, ctx)
        emu.launcher = 'perl'
        emu.fileext = 'pl'
        emu.programs = msg[4:len(msg)].rstrip('```').lstrip('```perl').lstrip('```pl')
        await self.run_emulator(ctx, emu)
    

    @commands.command()
    async def timeout(self, ctx, msg):
        """ プログラム制限時間を設定するぞ！ """
        if msg.isalnum() and msg.isdecimal():
            if int(msg) > 600:
                await ctx.send(ctx.author.mention + ' 制限時間を10分以上にはできないぞ！')
            elif int(msg) < 10:
                await ctx.send(ctx.author.mention + ' 制限時間を10秒未満にはできないぞ！')
            else:
                old_time = self.timeout
                self.timeout = int(msg)
                await ctx.send(ctx.author.mention + ' 制限時間を、'+ str(old_time) +'秒から'+ str(self.timeout)+'秒に変更したぞ！')
                log('[*] Timeout changed - '+ str(ctx.author) +': '+ str(old_time) +'s => ' + str(self.timeout) +'s')



def setup(bot):
    bot.add_cog(ProgrammingEmulator(bot))

