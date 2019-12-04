# -*- coding: utf-8 -*-
import discord
from discord.ext import tasks

import importlib
import threading
import time
import datetime
import random
import os, sys
import subprocess
import base64
import learn

TOKEN = ''


class ProgramInfo:
    def __init__(self):
        self.program = ''  # プログラム内容
        self.launcher = '' # プログラム実行ファイル
        self.fileext = ''  # プログラムファイル拡張子
        self.mention_flag = True # リプライするかどうか
        self.session_id = random.randint(0, 9999) # セッションID
        self.version = '1.3'
        self.lang = ''
    
    def get_filepath(self):
        if os.name == 'nt':
            return os.path.dirname(os.path.abspath(__file__)) + '\\index.' + self.fileext
        else:
            return os.path.dirname(os.path.abspath(__file__))+ '/index.' + self.fileext


def get_mentions():
    mention_dict = {}
    for member in client.get_all_members():
        mention_dict[member.name] = member.mention
    return mention_dict


def log(data, session_id):
    try:
        dt_now = datetime.datetime.now()
        print('['+ str(dt_now) +' - '+ str(session_id) +'] '+ data)
    except Exception as e:
        print('['+ str(dt_now) +' - '+ str(session_id) +'] [-] '+ str(e.args))


timed_out = False
timeout = 30
def moniter_process(proc):
    global timed_out
    global timeout
    timed_out = False
    count = 0
    while True:
        count += 1
        time.sleep(1)
        if proc.poll() is not None:
            break
        if count > timeout:
            proc.kill()
            timed_out = True
            break

client = discord.Client()

@client.event
async def on_ready():
    log("[*] progracat bot started. - v" + ProgramInfo().version, 'started')

@client.event
async def on_message(message):
    global timed_out
    global timeout
    if message.author.bot: # Botによる反応は除外
        return
    
    # 初期化
    cmd = message.content.split(':')[0].lower()
    program_lang_list = ['/py', '/pyw', '/rb', '/rbw', '/js', '/jsw', '/php', '/phpw', '/pl', '/plw']
    program = ''
    info = ProgramInfo()
    
    # コマンド分析
    if cmd in program_lang_list:
        # プログラム言語検出
        # Python
        if cmd == '/py':
            program = message.content[4:len(message.content)].rstrip('```').lstrip('```python').lstrip('```py')
            info.lang = 'Python'
            info.launcher = 'python3'
            info.fileext = 'py'
        elif cmd == '/pyw':
            program = message.content[5:len(message.content)].rstrip('```').lstrip('```python').lstrip('```py')
            info.mention_flag = False
            info.lang = 'Python'
            info.launcher = 'python3'
            info.fileext = 'py'
        
        # Ruby
        elif cmd == '/rb':
            program = message.content[4:len(message.content)].rstrip('```').lstrip('```ruby').lstrip('```rb')
            info.lang = 'Ruby'
            info.launcher = 'ruby'
            info.fileext = 'rb'

        elif cmd == '/rbw':
            program = message.content[5:len(message.content)].rstrip('```').lstrip('```ruby').lstrip('```rb')
            info.mention_flag = False
            info.lang = 'Ruby'
            info.launcher = 'ruby'
            info.fileext = 'rb'
        
        # Node.js
        elif cmd == '/js':
            program = message.content[4:len(message.content)].rstrip('```').lstrip('```js')
            info.lang = 'JavaScript'
            info.launcher = 'node'
            info.fileext = 'js'
        elif cmd == '/jsw':
            program = message.content[5:len(message.content)].rstrip('```').lstrip('```js')
            info.mention_flag = False
            info.lang = 'JavaScript'
            info.launcher = 'node'
            info.fileext = 'js'

        # PHP
        elif cmd == '/php':
            program = message.content[5:len(message.content)].rstrip('```').lstrip('```php')
            info.lang = 'PHP'
            info.launcher = 'php'
            info.fileext = 'php'
        elif cmd == '/phpw':
            program = message.content[6:len(message.content)].rstrip('```').lstrip('```php')
            info.mention_flag = False
            info.lang = 'PHP'
            info.launcher = 'php'
            info.fileext = 'php'

        # Perl
        elif cmd == '/pl':
            program = message.content[6:len(message.content)].rstrip('```').lstrip('```perl').lstrip('```pl')
            info.lang = 'Perl'
            info.launcher = 'perl'
            info.fileext = 'pl'
        elif cmd == '/plw':
            program = message.content[7:len(message.content)].rstrip('```').lstrip('```perl').lstrip('```pl')
            info.mention_flag = False
            info.lang = 'Perl'
            info.launcher = 'perl'
            info.fileext = 'pl'
        
        if info.mention_flag:
            await message.channel.send(message.author.mention +' '+ info.lang +'のプログラム受け取ったぞ！ちょっと待ってて...')
        else:
            await message.add_reaction('👌')
        log('[*] '+ str(message.author) +': "'+ program +'"', info.session_id)

        # メンション辞書追加
        if info.fileext == 'py':
            program = '# -*- coding: utf-8 -*-\r\nmentions = ' + str(get_mentions()) + '\r\n' + program
        elif info.fileext == 'rb':
            program = 'mentions = ' + str(get_mentions()).replace("': '", "' => '") + ';\r\n' + program
        elif info.fileext == 'js':
            program = 'var mentions = ' + str(get_mentions()) + '\r\n' + program
        elif info.fileext == 'php':
            program = '<?php\r\n$mentions = array(' + str(get_mentions()).replace("': '", "' => '").rstrip('}').lstrip('{') + ');\r\n' + program
        elif info.fileext == 'pl':
            program = 'use strict;\r\nuse warnings;\r\nmy %mentions = (' + str(get_mentions()).replace("': '", "' => '").rstrip('}').lstrip('{') + ');\r\n' + program
        
        # プログラム実行
        try:   
            # ファイル書き込み
            with open(info.get_filepath(), 'w', encoding='utf-8') as f:
                f.write(program)
            
            # プロセス起動
            proc = subprocess.Popen([info.launcher, info.get_filepath()], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # プロセス監視スレッド開始
            th =threading.Thread(target=moniter_process, args=(proc, ))
            th.start()
            log('[*] Process started. timeout:'+ str(timeout) +'s', info.session_id)

            # 実行データ取得
            try:
                output = proc.stdout.read().decode('utf-8')
            except:
                output = proc.stdout.read().decode('shift-jis')
            
            # 制限時間内に終了しなかったら強制終了
            if timed_out and info.mention_flag:
                await message.channel.send(message.author.mention + ' 疲れたからもう終わらすね！')
            elif timed_out:
                await message.add_reaction('🥱')
            if timed_out:
                log('[+] Program timed out. ', info.session_id)
                return
            
            # トークン情報が入っていたら
            if output.find(TOKEN) != -1:
                if info.mention_flag:
                    await message.channel.send(message.author.mention + ' ボクのトークンは渡さないよ！😠')
                else:
                    await message.add_reaction('😠')
                log('[!] '+ str(message.author) +': Stole token detected!', info.session_id)
                return

            # 実行データ送信
            if info.mention_flag:
                await message.channel.send(message.author.mention + output)
            else:
                if output.strip() == '':
                    await message.add_reaction('🥴')
                else:
                    await message.channel.send(output)
            
            log('[+] Program exited. ', info.session_id)
        except Exception as e:
            if info.mention_flag:
                await message.channel.send(message.author.mention +' うぬぬ、エラーだぞ...: '+ str(e.args))
            else:
                await message.add_reaction('😖')
            log('[-] Error: '+ str(e.args), info.session_id)

    elif message.content == 'ぬるぽ':
        log('[*] '+ str(message.author) +': NullPointerException', info.session_id)
        await message.channel.send(message.author.mention +'■━⊂( ･∀･) 彡 ｶﾞｯ☆`Д´)ﾉ')

    elif message.content == '/help':
        data = '```md\r\n'
        data += '<progracat bot - v'+ info.version +'>\r\n'
        data += '* こんにちは！たくさんのプログラミング言語を知ってるプログラキャットだよ！\r\n'
        data += '* それぞれ書いたプログラムをコマンドと一緒に投げてくれたら、実行結果を答えるぞ！\r\n'
        data += '* 俺はオープンソースだぞ！コマンド一覧とかソースコード見たいなら、↓からアクセスしてくれ！\r\n'
        data += '+ 今知ってる言語は、Python, Ruby, PHP, JavaScript, Perlだよ！\r\n'
        data += '* /talk コマンドで何かしゃべるぞ！'
        data += '```\r\n'
        data += 'https://github.com/betacode-projects/DiscordBot/tree/master/progracat \r\n'

        log('[*] '+ str(message.author) +': Shown help.', info.session_id)
        await message.channel.send(message.author.mention + data)   

    elif cmd == '/timeout':
        tmp = message.content.split(':')
        if len(tmp) == 2:
            if tmp[1].isalnum() and tmp[1].isdecimal():
                if int(tmp[1]) > 600:
                    await message.channel.send(message.author.mention + ' 制限時間を10分以上にはできないぞ！')
                elif int(tmp[1]) < 10:
                    await message.channel.send(message.author.mention + ' 制限時間を10秒未満にはできないぞ！')
                else:
                    old_time = timeout
                    timeout = int(tmp[1])
                    await message.channel.send(message.author.mention + ' 制限時間を、'+ str(old_time) +'秒から'+ str(timeout)+'秒に変更したぞ！')
                    log('[*] Timeout changed - '+ str(message.author) +': '+ str(old_time) +'s => ' + str(timeout) +'s', info.session_id)
    
    elif message.content == '/comp':
        try:
            learn.compile_text()
            await message.channel.send(message.author.mention + ' 言語データを再コンパイルしたぞ！')
            log("[*] Languages data recompiled.", info.session_id)
        except Exception as e:
            await message.channel.send(message.author.mention + ' コンパイル失敗したぞ...: '+ str(e.args))
            log('[-] Error: '+ str(e.args), info.session_id)

    elif cmd == '/comp':
        tmp = message.content.split(':')
        if len(tmp) == 2:
            if tmp[1].isalnum() and tmp[1].isdecimal():
                if 0 < int(tmp[1]) < 10:
                    try:
                        learn.compile_text(int(tmp[1]))
                        await message.channel.send(message.author.mention + ' 言語データを再コンパイルしたぞ！')
                        log("[*] Languages data recompiled. (state="+ tmp[1] +")", info.session_id)
                    except Exception as e:
                        await message.channel.send(message.author.mention + ' コンパイル失敗したぞ...: '+ str(e.args))
                        log('[-] Error: '+ str(e.args), info.session_id)


    elif message.content == '/talk':
        await message.channel.send(learn.get_massage())
        log('[*] '+ str(message.author) +': Talk to me. (140 words)', info.session_id)

    elif cmd == '/talk':
        tmp = message.content.split(':')
        if len(tmp) == 2:
            if tmp[1].isalnum() and tmp[1].isdecimal():
                if int(tmp[1]) > 600:
                    await message.channel.send(message.author.mention + ' 600文字以上はしゃべれないぞ...')
                elif int(tmp[1]) < 30:
                    await message.channel.send(message.author.mention + ' 30文字以下はしゃべれないぞ...')
                else:
                    words = int(tmp[1])
                    await message.channel.send(learn.get_massage(words))
                    log('[*] '+ str(message.author) +': Talk to me. ('+ str(words) +' words)', info.session_id)


    elif message.content == '/version':
        log('[*] '+ str(message.author) +': Shown version.', info.session_id)
        await message.channel.send(message.author.mention + 'バージョンは'+ info.version +'だぞ！')

    elif message.content.find('完全に理解した') != -1:
        await message.add_reaction('🤔')

    elif message.content.find('炎上') != -1:
        await message.add_reaction('🔥')
    
    elif message.content.find('ハゲ') != -1:
        await message.channel.send(message.author.mention + 'また髪の話してる...(´･ω･`)')
        log('[*] '+ str(message.author) +': "Hage" detected.', info.session_id)

    elif message.content.find('ネコ') != -1:
        await message.add_reaction('😼')

    elif message.content.find('眠い') != -1:
        await message.add_reaction('😪')

    elif message.content.find('社畜') != -1:
        await message.add_reaction('😇')

    elif message.content.find('スパゲッティコード') != -1 or message.content.find('スパゲティーコード') != -1 or message.content.find('スパゲッティーコード') != -1:
        await message.add_reaction('😨')

    elif message.content.find('プログラキャット') != -1 or message.content.find('progracat') != -1:
        await message.channel.send(message.author.mention + '(=^. .^=)ﾐｬｰ')
    
    elif message.content.find('尊い') != -1:
        await message.add_reaction('☺️')
    
    elif message.content.find('おめ！') != -1 or message.content.find('おめ!') != -1 or message.content.find('おめでとう') != -1:
        await message.add_reaction('🥳')
    
    else:
        txt_dir = os.path.dirname(os.path.abspath(__file__)) + '/text'
        with open(txt_dir + '/discord.txt', 'a', encoding='utf-8') as f:
            f.write('\n' + message.content)


# Discordのメッセージデータを言語データに反映
@tasks.loop(seconds=60*60*24)
async def recompile_text_loop():
    try:
        learn.compile_text()
        log("[*] Languages data recompiled.", 'compiled')
    except Exception as e:
        log("[-] Compile Error.", str(e.args))



if __name__ == "__main__":
    recompile_text_loop.start()
    client.run(TOKEN)
