import requests
def main(train_no):
    try:
        cookies = {
            'PHPSESSID': 'jukhvmopi3qidfvsp79n3tft91',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://search.brave.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            '^sec-ch-ua': '^\\^Brave^\\^;v=^\\^125^\\^, ^\\^Chromium^\\^;v=^\\^125^\\^, ^\\^Not.A/Brand^\\^;v=^\\^24^\\^^',
            'sec-ch-ua-mobile': '?0',
            '^sec-ch-ua-platform': '^\\^Windows^\\^^',
        }
        link=f'https://etrain.info/train/{train_no}/map'
        response = requests.get(link, headers=headers, cookies=cookies)
        from bs4 import BeautifulSoup
        tag=BeautifulSoup(response.content,'html.parser')
        data=tag.find('div',{'id':'lowerdata'})
        return data
    except:
        return None