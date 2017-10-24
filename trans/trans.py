import argparse
import sys
from termcolor import colored, cprint

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
    cmd_print(trans_result, args.more)


def cmd_print(trans_result, more=False):
    cprint('')
    cprint('  ' + trans_result['keyword'], 'cyan', end='\t', attrs=['bold'])
    if(len(trans_result['phonetic_list']) <= 1):
        cprint(' '.join(trans_result['phonetic_list']), 'magenta', end='\n\n')
    else:
        cprint('英' + trans_result['phonetic_list'][0] + ' 美' +
               trans_result['phonetic_list'][1], 'magenta', end='\n\n')
    for item in trans_result['trans_list']:
        cprint('- ' + item, 'yellow', end='\n')
    cprint('')
    num = 1
    for item in trans_result['phrase_list']:
        cprint(str(num) + '. ',end='')
        str_value=item[0].replace(trans_result['keyword'],'\1')
        for word in str_value:
            if word == '\1':
                cprint(trans_result['keyword'],'cyan',end='')
            else:
                cprint(word,end='')
        cprint('\n  ' + item[1], 'blue')
        if num == 4:
            break
        num += 1
    if more:
        cprint('')
        num = 1
        for item in trans_result['bilingual_list']:
            cprint(str(num) + '. ',end='')
            str_value=item[0].replace(trans_result['keyword'],'\1')
            for word in str_value:
                if word == '\1':
                    cprint(trans_result['keyword'],'cyan',end='')
                else:
                    cprint(word,end='')
            cprint('\n  ' + item[1], 'magenta')
            num += 1


if __name__ == '__main__':
    execute()
