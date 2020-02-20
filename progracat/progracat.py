import discord
from discord.ext import commands
from discord.ext import tasks

import datetime
import traceback
import os, sys

FUNC_EXTENSIONS = ['mods.programs.main', 'mods.other.main', 'mods.game.main', 'mods.func.pokemon', 'mods.func.watch']
__version__ = 'v2.6.0'


def log(data):
    try:
        dt_now = datetime.datetime.now()
        print('['+ str(dt_now) +'] '+ data)
    except Exception as e:
        print('['+ str(dt_now) +'] [-] '+ str(e.args))


class Progracat(commands.Bot):

    def __init__(self, cmd_prefix, help_cmd):
        super().__init__(cmd_prefix, help_cmd)

        for cog in FUNC_EXTENSIONS:
            try:
                self.load_extension(cog)
            except:
                traceback.print_exc()
                pass
    
    """
    存在しないコマンドが呼び出された時のイベント
    """
    async def on_command_error(self, error, ctx):
        pass

    """
    Bot起動時のイベント
    """
    async def on_ready(self):
        log('[*] progracat bot started. - '+ __version__)


class HelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "ヘルプ"
        self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"
    
    def get_ending_note(self):
        return ("コマンド打つときは最初に'/'を付けるんだぞ！\r\n"
                "今のバージョンは、"+ __version__ +"だぞ！\r\n```"
                "https://github.com/betacode-projects/DiscordBot/tree/master/progracat ```")


if __name__ == "__main__":
    bot = Progracat('/', HelpCommand())
    bot.run(sys.argv[1])
