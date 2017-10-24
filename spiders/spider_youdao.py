import requests
from bs4 import BeautifulSoup

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"}


def crawl(keyword):
    url = 'http://dict.youdao.com/search?q={}&keyfrom=fanyi.smartResult'.format(
        keyword)
    html = requests.get(url, headers=headers, timeout=10).text
    soup = BeautifulSoup(html, 'lxml').find('div', id='results-contents')
    result = {
        'keyword': keyword
    }
    phrs_tab = soup.find('div', id='phrsListTab')
    phonetic_items = phrs_tab.find_all('span', {'class': 'phonetic'})
    phonetic_list = []
    for item in phonetic_items:
        value = item.get_text().replace('\r', '').replace('\n', '')
        phonetic_list.append(value)
    result['phonetic_list'] = phonetic_list
    trans_container = phrs_tab.find(
        'div', {'class': 'trans-container'}).find('ul')
    trans_list = []
    for item in trans_container.find_all('li'):
        value = item.get_text().replace('\r', '').replace('\n', '')
        trans_list.append(value)
    for item in trans_container.find_all('p'):
        value = item.get_text().replace('\r', '').replace('\n', '')
        trans_list.append(value)
    result['trans_list'] = trans_list
    web_phrase_items = soup.find('div', id='webPhrase').find_all(
        'p', {'class': 'wordGroup'})
    phrase_list = []
    for item in web_phrase_items:
        try:
            content_title = item.find(
                'span', {'class': 'contentTitle'}).get_text()
            value = item.get_text().replace(content_title, '').replace(
                '\r', '').replace('\n', '').replace('\t', '').replace('  ', '')
        except:
            continue
        phrase_list.append([content_title, value])
    result['phrase_list'] = phrase_list
    example_items = soup.find('div', id='bilingual').find('ul').find_all('li')
    bilingual_list = []
    for item in example_items:
        try:
            tags = item.find_all('p')
            src_value = tags[0].get_text().replace('\r','').replace('\n','')
            trans_value = tags[1].get_text().replace('\r','').replace('\n','')
        except:
            continue
        bilingual_list.append([src_value, trans_value])
    result['bilingual_list'] = bilingual_list
    return result


def translate(keyword):
    try:
        result = crawl(keyword)
    except:
        result = {}
    return result


if __name__ == '__main__':
    print(translate('翻译'))
    print(translate('try'))
