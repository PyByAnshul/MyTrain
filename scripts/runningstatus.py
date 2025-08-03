import requests 
# from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
from datetime import datetime
def main(train_number,date):
    if type(date)==str:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    date=re.sub('[^a-zA-Z0-9]','',str(date))
    #print(date)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Referer': 'https://runningstatus.in/status/20411-on-20231224',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '^\\^Not_A',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
    }

    params = (
        ('a', 'status'),
        ('trainno', train_number),
        ('date', date),
    )

    response = requests.get('https://runningstatus.in/check.php', headers=headers, params=params)
    tag=BeautifulSoup(response.text,'html.parser')
    table=tag.find('table',{'class':'table table-bordered table-responsive'})
    return table

# date=datetime.now().date()
# main('22458',date)