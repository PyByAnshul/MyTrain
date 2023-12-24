import requests
from pymongo import MongoClient
from datetime import datetime


def main(source_code,dist_code,date):
    if type(date)==str:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    
    date = date.strftime("%d-%m-%Y")
    print(date)
    headers = {
        'authority': 'www.trainman.in',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.8',
        'sec-ch-ua': '^\\^Not_A',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    }
    cookies={'bm_mi':'011FD2E727706DD6D1B9E0AB92AD4F1B~YAAQTwXUF4IF5YWMAQAAtJ/UlRblUXksIKXQnehY7XsnIN4lFfHqygd2y10wD29LRLVICP4ao+a5JnoAckJzIWDtEEneqnHKOzqGQzbBPBuKkvar96AfOO/vcxqKKIapzLDgfDImXW8iRjigo0yOAQMKGhCdo2rrckiO63mI0qhwG14nKWepJrWgZ7DQBs6cTO0IrsEFy49k5KbFZaxmU3XkO6WmQndI5Q7kZAJCi6DXX8P8+fB2ey/lRsf/EJA66BQDX+xzB3Zfsu31OjX0CyyjBkBy5U1ONYWs+9Zcd7C02m8Io1wFxUHbOgqcB7jqmg==~1' ,'bm_sv':'38E9332D391F328357019E3D61A4ACC7~YAAQTwXUF4oF5YWMAQAAH6PUlRaCt+kq65aHqpu0pS1TbTaYS21RaCq+ILbeAsjrWEsqQ4DWRO58p7c0I2bcIFw2Nz31reZy1ziS8C63SYE4bcrW4DAdrj0OVA2P39dQTztfaVNK8BhkWcnCBMkoMzGawmlDQxL9ABaG/miRggXaRAV0M6MJH2jkDLwCh8n6hzXD6pmkY28qSlsir0xI2hTPXg414YI2MfO6b0MILGVWHpfktu4Y+UzqbXj9m8qbzhI=~1','ak_bmsc':'152AAF6C83E6A179E7A5EB8937693847~000000000000000000000000000000~YAAQTwXUF0cc5YWMAQAAjdPnlRZuwwv1KBXGkM49kqcRHtaZqNL0lULod3atfOR08FtGOgex6MvoNiVIGj07PhoK8m6kRrWshjRZqxZ3Ad4MoYiaDx2RRDZKWQlHCfY/dkK8PcoDR2+ncifMLtA5TZzpbOBGS0GjLdD7+DJ5NPZF3rNeM91FDwkTLzN5GM5xbh3exHImGB11HCiAWvnd8RYeBNxv3sr84FtRmTCOpO38R5Kn1AILrkHxM/TqLqiwnjhU56rWf0UddxaOq4OsQTZ3JESf7dew9PjJh+mPZMo/UfOq9MCxyozUy7mWwQhbvjU+vRoDlNsPB6TG/i7heo9Tj+To6w7YjSYHVfQ5icoyeoLfvglAO+NNcQ4hpPRsjefAVBqdkfgmNVfoLALq8iX9QFZOJrMFRwIKpRsw5fMJNWXWqw==', 'AKA_A2':'A'}
    params = (
        ('key', '012562ae-60a9-4fcd-84d6-f1354ee1ea48'),
        ('sort', 'smart'),
        ('meta', 'true'),
        ('class', 'ALL'),
        ('date', f'{date}'),
        ('quota', 'GN'),
    )
    try:
        response = requests.get(f'https://www.trainman.in/services/trains/{source_code}/{dist_code}', headers=headers, params=params,cookies=cookies)
        
    except requests.exceptions:
        print('excepipi')
        return {}
    print(response.json())
    return {'response':dict(response.json())}


# da=main('DLI','MOZ',datetime.now().date())
# print(da)