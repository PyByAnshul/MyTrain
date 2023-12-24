import requests
from datetime import datetime
def main(source,dist,date):
    if type(date)==str:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    
    date = date.strftime("%d-%m-%Y")
    print(date)
    headers = {
        'authority': 'www.railyatri.in',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'web_loc_user_id=-1702720953; _railyatri_web=c9270a902ef16bf8b9e46d1f3b87e5f1; utm=dwebhome_header_tbs+; utm_source=dwebhome_header_tbs+; userId=-1702720953; user_id=-1702720953; ets_railyatri=^{^%^22ecomm_type^%^22:^%^22train_ticket_booking^%^22^%^2C^%^22step^%^22:^%^22New_TBS_tbs_loaded^%^22^%^2C^%^22booking_id^%^22:^%^22^%^22^%^2C^%^22user_id^%^22:^%^22-1702720953^%^22^%^2C^%^22src^%^22:^%^22tbs^%^22^%^2C^%^22utm_referrer^%^22:^%^22dwebhome_header_tbs+^%^22^%^2C^%^22device_type_id^%^22:4^%^2C^%^22from_station^%^22:^%^22MFP^%^22^%^2C^%^22to_station^%^22:^%^22NDLS^%^22^%^2C^%^22journey_date^%^22:^%^222023-12-23T00:00:00.000Z^%^22^%^2C^%^22number_of_trains^%^22:11^%^2C^%^22filters_applied^%^22:^%^22Quota(General)^%^20^%^22^%^2C^%^22original_from^%^22:^%^22MFP^%^22^%^2C^%^22original_to^%^22:^%^22NDLS^%^22^%^2C^%^22btb_organisation_id^%^22:null^%^2C^%^22v_code^%^22:null^}; Railyatri_Route_Info=^{^%^22from^%^22:^{^%^22name^%^22:^%^22MUZAFFARPUR^%^20JN^%^22^%^2C^%^22code^%^22:^%^22MFP^%^22^}^%^2C^%^22to^%^22:^{^%^22name^%^22:^%^22NEW^%^20DELHI^%^22^%^2C^%^22code^%^22:^%^22NDLS^%^22^}^%^2C^%^22date^%^22:^%^222023-12-23T00:00:00.000Z^%^22^%^2C^%^22filter^%^22:^{^%^22CNF^%^22:false^%^2C^%^22AC^%^22:false^%^2C^%^22NONAC^%^22:false^%^2C^%^22Quota^%^22:^{^%^22General^%^22:true^%^2C^%^22Tatkal^%^22:false^%^2C^%^22Ladies^%^22:false^%^2C^%^22LowerBirth^%^22:false^}^%^2C^%^22SortBy^%^22:^{^%^22Popularity^%^22:false^%^2C^%^22Departure^%^22:false^%^2C^%^22Arrival^%^22:false^%^2C^%^22OnTime_Performance^%^22:false^%^2C^%^22Duration^%^22:false^}^%^2C^%^22SelectedClass^%^22:^%^22^%^22^%^2C^%^22Departure^%^22:^%^22^%^22^%^2C^%^22Arival^%^22:^%^22^%^22^%^2C^%^22Origin^%^22:^%^22^%^22^%^2C^%^22Destination^%^22:^%^22^%^22^%^2C^%^22RemoveRefreshCards^%^22:false^}^%^2C^%^22userid^%^22:^%^22-1702720953^%^22^%^2C^%^22device^%^22:4^%^2C^%^22utm_source^%^22:^%^22dwebhome_header_tbs+^%^22^%^2C^%^22vCode^%^22:null^%^2C^%^22btbOrgId^%^22:null^%^2C^%^22btbUserId^%^22:null^%^2C^%^22number_of_trains^%^22:11^%^2C^%^22filters_applied^%^22:^{^%^22current^%^22:^%^22Quota(General)^%^20^%^22^}^%^2C^%^22src^%^22:^%^22tbs^%^22^%^2C^%^22busDetails^%^22:^{^%^22is_smart_route^%^22:false^}^%^2C^%^22authToken^%^22:^%^22^%^22^%^2C^%^22busTabDeeplink^%^22:null^}',
        'referer': 'https://www.google.com/',
        'sec-ch-ua': '^\\^Not_A',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    response = requests.get('https://www.railyatri.in/trains-between-stations', headers=headers)
    d=response.cookies.get_dict()
    params = (
        ('from', source),
        ('to', dist),
        # ('dateOfJourney', '23-12-2023'),
        ('dateOfJourney', str(date)),
        ('action', 'train_between_station'),
        ('controller', 'train_ticket_tbs'),
        ('device_type_id', '6'),
        ('from_code', source),
        ('from_name', ''),
        ('journey_date', '23-12-2023'),
        ('journey_quota', 'GN'),
        ('to_code', dist),
        ('to_name', ''),
        ('authentication_token', ''),
        ('v_code', 'null'),
        ('user_id',d.get('user_id')),
    )

    response = requests.get('https://api.railyatri.in/api/trains-between-station-from-wrapper.json', headers=headers, params=params)
    # print(response.json())
    return response.json()

# main('DLI',"MOZ",'25-12-2023')