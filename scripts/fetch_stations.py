import requests
from bs4 import BeautifulSoup
import traceback

def main(train_no):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.railmitra.com',
        'Referer': 'https://www.railmitra.com/train-schedule',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        '^sec-ch-ua': '^\\^Brave^\\^;v=^\\^125^\\^, ^\\^Chromium^\\^;v=^\\^125^\\^, ^\\^Not.A/Brand^\\^;v=^\\^24^\\^^',
        'sec-ch-ua-mobile': '?0',
        '^sec-ch-ua-platform': '^\\^Windows^\\^^',
    }

    data = {
    'train': train_no
    }
    try:
        
        response = requests.post('https://www.railmitra.com/train-schedule', headers=headers, data=data)
        tag=BeautifulSoup(response.text,'html.parser')
        table=tag.find('div',{'id':'trainSchedule'})
        links=table.find_all('a')

        text_list = [i.getText().strip() for i in links]
        # Output the text list
        return text_list
    except:
            traceback.print_exc()
            return ['none','none']