import requests
import json
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"}


def crawl(keyword):
    url = 'http://www.iciba.com/index.php?a=getWordMean&c=search&list=1%2C2%2C3%2C4%2C5%2C8%2C9%2C10%2C12%2C13%2C14%2C15%2C18%2C21%2C22%2C24%2C3003%2C3004%2C3005&word={}'.format(
        keyword)
    res_text = requests.get(url, headers=headers).text
    res_json_data = json.loads(res_text)
    result = {
        'keyword': keyword
    }

    phonetic_list = re.findall(
        "'ph_en': '(.*?)'", str(res_json_data['baesInfo']))
    phonetic_list += re.findall("'ph_am': '(.*?)'",
                                str(res_json_data['baesInfo']))
    phonetic_list += re.findall("'word_symbol': '(.*?)'",
                                str(res_json_data['baesInfo']))
    phonetic_list = ['[%s]' % item for item in phonetic_list]
    result['phonetic_list'] = phonetic_list

    symbols = res_json_data['baesInfo']['symbols'][0]['parts']
    trans_list = []
    for item in symbols:
        value = item['part'] + '；'.join(item['means'])
        trans_list.append(value)
    result['trans_list'] = trans_list

    phrase_list = []
    try:
        phrase_items = res_json_data['phrase']
    except:
        phrase_items = []
    for item in phrase_items:
        try:
            title = item['cizu_name']
            value = item['jx'][0]['jx_en_mean'] + \
                '  ' + item['jx'][0]['jx_cn_mean']
        except:
            continue
        phrase_list.append([title, value])
    result['phrase_list'] = phrase_list

    bilingual_list = []
    try:
        sentence_items = res_json_data['sentence']
    except:
        sentence_items = []
    for item in sentence_items:
        try:
            network_en = item['Network_en']
            network_cn = item['Network_cn']
        except:
            continue
        bilingual_list.append([network_en, network_cn])
    result['bilingual_list'] = bilingual_list
    return result


def translate(keyword):
    try:
        result = crawl(keyword)
    except:
        result = {}
    return result


if __name__ == '__main__':
    print(translate('just do it'))
