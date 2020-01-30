#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from glob import iglob
import re
import os

import MeCab
import markovify


def load_from_file(files_pattern):
    """read and merge files which matches given file pattern, prepare for parsing and return it.
    """

    # read text
    text = ""
    for path in iglob(files_pattern):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text += f.read().strip()
        except:
            with open(path, 'r', encoding='shift-jis') as f:
                text += f.read().strip()

    # delete some symbols
    unwanted_chars = ['\r', '\u3000', '-', '｜']
    for uc in unwanted_chars:
        text = text.replace(uc, '')

    # delete aozora bunko notations
    unwanted_patterns = [re.compile(r'《.*》'), re.compile(r'［＃.*］')]
    for up in unwanted_patterns:
        text = re.sub(up, '', text)

    return text


def split_for_markovify(text):
    """split text to sentences by newline, and split sentence to words by space.
    """
    # separate words using mecab
    mecab = MeCab.Tagger()
    splitted_text = ""

    # these chars might break markovify
    # https://github.com/jsvine/markovify/issues/84
    breaking_chars = [
        '(',
        ')',
        '[',
        ']',
        '"',
        "'",
        '<',
        '>'
    ]

    # split whole text to sentences by newline, and split sentence to words by space.
    for line in text.split():
        mp = mecab.parseToNode(line)
        while mp:
            try:
                if mp.surface not in breaking_chars:
                    splitted_text += mp.surface    # skip if node is markovify breaking char
                if mp.surface != '。' and mp.surface != '、':
                    splitted_text += ' '    # split words by space
                if mp.surface == '。':
                    splitted_text += '\n'    # reresent sentence by newline
            except UnicodeDecodeError as e:
                # sometimes error occurs
                print(line)
            finally:
                mp = mp.next

    return splitted_text


def load_discord_csv(files_pattern):
    csv_data = []
    for path in iglob(files_pattern):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    csv_data.append(line.split('"')[7])
                except:
                    pass
    
    if csv_data:
        with open(os.path.dirname(os.path.abspath(__file__)) + '/text/discord.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(csv_data))


def compile_text(state=2):
    # load discord csv
    now_directory = os.path.dirname(os.path.abspath(__file__))
    load_discord_csv(now_directory +'/text/*.csv')

    # load text
    rampo_text = load_from_file(now_directory + '/text/*.txt')

    # split text to learnable form
    splitted_text = split_for_markovify(rampo_text)

    # learn model from text.
    text_model = markovify.NewlineText(splitted_text, state_size=state)

    # save learned data
    with open(now_directory +'/learned_data.json', 'w') as f:
        f.write(text_model.to_json())


def get_massage(words=140):
    now_directory = os.path.dirname(os.path.abspath(__file__))
    message = ''

    # 言語データがない場合はデータをコンパイルする
    if not(os.path.exists(now_directory +'/learned_data.json')):
        compile_text()
    
    with open(now_directory +'/learned_data.json') as f:
        text_model = markovify.NewlineText.from_json(f.read())

    for i in range(100):
        # ... and generate from model.
        sentence = text_model.make_short_sentence(words)

        if sentence != None:
            message = ''.join(sentence.split())   # need to concatenate space-splitted text
            break

    return message


if __name__ == '__main__':
    print(get_massage())
