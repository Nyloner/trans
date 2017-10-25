import argparse
import re
from termcolor import cprint

from trans.spiders import spider_youdao


def execute():
    parser = argparse.ArgumentParser(
        description='A simple tool for translation.')
    parser.add_argument('keyword')
    parser.add_argument('-m', '--more', action="store_true",
                        help='show more information.')
    args = parser.parse_args()
    keyword = args.keyword
    trans_result = spider_youdao.translate(keyword)
    cmd_print(keyword, trans_result, args.more)


def highlight_keyword(keyword, text, color='cyan'):
    word_list = re.findall(keyword, text, flags=re.IGNORECASE)
    for word in word_list:
        text = text.replace(word, '\1' + word + '\1')
    flag = False
    for char in text:
        if char == '\1':
            flag = not flag
            continue
        if flag:
            cprint(char, color, end='', attrs=['bold'])
        else:
            cprint(char, end='')


def cmd_print(keyword, trans_result, more=False):
    cprint('')
    if trans_result == {}:
        cprint(keyword, 'cyan', attrs=['bold'])
        cprint('\nCome To Nothing.', 'magenta', attrs=['bold'])
        return

    cprint('  ' + keyword, 'cyan', end='\t', attrs=['bold'])
    if len(trans_result['phonetic_list']) <= 1:
        cprint(' '.join(trans_result['phonetic_list']), 'magenta', end='\n\n')
    else:
        cprint('英' + trans_result['phonetic_list'][0] + ' 美' +
               trans_result['phonetic_list'][1], 'magenta', end='\n\n')

    for item in trans_result['trans_list']:
        cprint('- ' + item, 'yellow', end='\n')

    cprint('')
    num = 1
    for item in trans_result['phrase_list']:
        cprint(str(num) + '. ', end='')
        highlight_keyword(keyword, item[0])
        cprint('\n  ' + item[1], 'blue')
        if num == 4:
            break
        num += 1

    if more:
        cprint('')
        num = 1
        for item in trans_result['bilingual_list']:
            cprint(str(num) + '. ', end='')
            highlight_keyword(keyword, item[0])
            cprint('\n  ' + item[1], 'magenta')
            num += 1


if __name__ == '__main__':
    execute()
