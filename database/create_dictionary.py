import string, requests
from bs4 import BeautifulSoup


main_link = 'https://dictionary.cambridge.org/browse/english/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru',
    'Connection': 'keep-alive',
    'Host': 'dictionary.cambridge.org',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
}
# 'Referer': 'https://dictionary.cambridge.org/browse/english-russian/a/',
# Cookie: cto_bidid=GGI3FF9VMTZvMGxoWGxSS0clMkJwOXpodXRublFtZ0JJJTJCJTJGblp5Ym9zMThrVEE3WnNMa1oxMUVQJTJCMSUyRjJSNU9GQzdlZWNHRVZocVM0Z1d6NzNyOE5aJTJCV3FYSXhPZyUzRCUzRA; cto_bundle=YjCbnV9Gbk1iNU0zZGpDaWZvVkczVjFzQTZZNnR5YUxkOWo1aTg2N1lRUFFrNjhRQlRlazd5ZzFzNWFnZXFodkt5SnRoaFd3V051UkM4Mm1LNW1RV3ZxaEVmdlFIR2FTZjhjNHZ3T21YNUc1b21TTEJaZ2tNVldRVXYlMkZBbG9MRGxSMDc5; _hjAbsoluteSessionInProgress=1; _hjSession_2790984=eyJpZCI6ImI5MmYzZTc4LWI0YjktNGY3Yi1iMWY0LTQ0M2FkYjY1M2MxMiIsImMiOjE3MDM1MDk5NzUyOTEsInMiOjAsInIiOjAsInNiIjoxfQ==; _sp_id.7ecc=3943d35c-c281-410e-9651-6029a667ae66.1703439111.4.1703512447.1703501328.653ca3d5-ca85-4f10-90ed-850a6b457ed7.d327fe90-b24d-4cdc-b5ac-f19ab321b2d1.573d493d-57b8-4fc3-90b6-2b8bdc00353e.1703509974980.53; _sp_ses.7ecc=*; _hjIncludedInSessionSample_2790984=0; _ga_L9GCR21SZ7=GS1.3.1703509974.4.1.1703512272.20.0.0; iawpvc1m=1; cto_bidid=bMawKl9VMTZvMGxoWGxSS0clMkJwOXpodXRublFtZ0JJJTJCJTJGblp5Ym9zMThrVEE3WnNMa1oxMUVQJTJCMSUyRjJSNU9GQzdlZWNHRVM1NGNsZGZUNzliZGQzVzdkcjcwNEElM0QlM0Q; cto_bundle=cS6GyV9Gbk1iNU0zZGpDaWZvVkczVjFzQTZhVlFwOGtja1RtU2tLMUZoV2p5N1R0aEp5empONmIxQ0pwQTF0MXBUOWtQTFBVbXQ4Q1hpS0NyZG1kWHdrdlprM3Btc1h3RzN3ZzclMkJLJTJCUEtZN1pTUUwzMldQU0Y3eTJYeUVueHhOWVAlMkJSVg; cto_bundle=Tq3p3l9Gbk1iNU0zZGpDaWZvVkczVjFzQTZUWFJ5YTdBaHZZako0MWQzczJDbkp5ZkF2Z0F5QiUyRjhIbkxXV05kJTJCMUVhNlRENEVMMzVHT1pBU0JiSHQ2VGl0TVRsZEpOV01pYUxKY1BnWVBiJTJCanVNZnNRY2RHRG1Na09xNzNRV2taQ2dESA; _fbp=fb.1.1703439117550.1685720706; _hjSessionUser_2790984=eyJpZCI6IjVjYzNkM2ZjLTQ1NzktNTc1My1hNzdmLTMxZmFmNzU5MGJkOSIsImNyZWF0ZWQiOjE3MDM0MzkxMTc1NjUsImV4aXN0aW5nIjp0cnVlfQ==; amp-access=amp-y6LztoV6SMKVRnaqiaakig; OptanonAlertBoxClosed=2023-12-25T13:50:55.099Z; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Dec+25+2023+15%3A50%3A55+GMT%2B0200+(%D0%98%D0%B7%D1%80%D0%B0%D0%B8%D0%BB%D1%8C%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=IL%3BTA; _ga=GA1.3.1967876603.1703439115; _hjHasCachedUserAttributes=true; iawpvc=28; iawpvccs=2; iawpvtc1m=28; FCNEC=%5B%5B%22AKsRol962ObkFlF4VDIMajjEvdAdp3Bu9AUdBm5O6VAzqFNmU6sRIK1s3fzf6t96cSb3naxKZU7kpFNvyYw7zzeWsokG5C8vMsOBF2SkpTo_QimOgr9nlLgapWIMMcjE2K3NdckmihV9Iz23g4mNThOyIhzc5f3fkg%3D%3D%22%5D%2Cnull%2C%5B%5B5%2C%22388%22%5D%5D%5D; iawsc1m=2; __gads=ID=76a6c1594be5588f:T=1703439119:RT=1703512140:S=ALNI_MaydJkS-FZDpvr68D9_qfM-c7l8FQ; __gpi=UID=00000d27cec06f93:T=1703439119:RT=1703512140:S=ALNI_MYLmZkUJ-dXMPXli1lywR2sG9dqDQ; cto_bundle=RH9coV9Gbk1iNU0zZGpDaWZvVkczVjFzQTZkRTc2UWlnMzFhOVF6ZGhyUDdkWW4yS2Q2JTJCdEFwdGJXN1M2OEdpSW5RZDhzT2VsTFRWYXNuTk1UTXltaVpDTmklMkI4JTJGdXcyS20wREd5RzJ3MHJHbjQlMkJ3cXVGYjQyb1ZFT2VtSFlIMzRMYjVz; _lr_env_src_ats=false; _lr_retry_request=true; loginPopup=4; pbjs-unifiedid=%7B%22TDID%22%3A%22a7966b79-7cb4-4d07-b37a-103f69b273fa%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-12-24T17%3A32%3A01%22%7D; pbjs-unifiedid_cst=zix7LPQsHA%3D%3D; _sharedID=d8d86ccd-9913-4229-9094-2abef731e7a3; _sharedID_cst=zix7LPQsHA%3D%3D; iawppid=8cc3246e1b464eb7888d7848eaeda12e; preferredDictionaries="english,british-grammar,english-arabic,english-turkish"; XSRF-TOKEN=46e29695-a8fe-405d-85ef-c81c4454e32c

def take_words(list_words_links, headers):
    for link in list_words_links:
        page = requests.get(link.get('href') if 'http://' in link.get('href')
                            else 'https://dictionary.cambridge.org' + link.get('href'), headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        definitions = soup.find_all('div', class_='di-title')
        definitions = definitions[1:]
        for d in definitions:
            print(d.text)
        # with open('test.html', 'w') as file:
        #     file.write(str(page.content))
        break

def read_words_pages(words_links, headers, c):

    for link in words_links:
        page = requests.get(link.get('href'), headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        list_words_links = soup.find_all('a', class_=["tc-bd"])
        list_words_links = filter(lambda l: '/dictionary/english-russian/' + c in l.get('href'), list_words_links)
        # print(len(list_words_links))
        for lk in list_words_links:
            print(lk.get('href'))
        # take_words(list_words_links, headers)
        # break


def inner_layer_links(root_links, headers, c):

    for link in root_links:
        page = requests.get(link.get('href'), headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        word_links = soup.find_all('a')
        word_links = filter(lambda l: link.get('href') in l.get('href')
                       and link.get('href') != l.get('href'), word_links)
        # read_words_pages(word_links, headers, c)
        # break


def main(root_link, headers):

    for c in string.ascii_lowercase:
        page = requests.get(root_link + c, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.find_all('a')
        links = filter(lambda l: (root_link + c) in l.get('href')
                       and (root_link + c) != l.get('href'), links)
        inner_layer_links(links, headers, c)
        # break



if __name__ == "__main__":
    import nltk
    nltk.download('words')
    from nltk.corpus import words

    english_words = set(words.words())
    print(len(english_words))
