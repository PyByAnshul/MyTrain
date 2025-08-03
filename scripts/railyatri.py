import requests
from bs4 import BeautifulSoup
import traceback

def main(train_no):
    try:
        response = requests.get("https://www.railyatri.in/time-table/"+train_no)
        # #print(response.content)
        tag=BeautifulSoup(response.content,'html.parser')
        div=tag.find('div',{'class':'timetable_white_timeline_bg__O68X3 MuiBox-root css-0'})

        return div
    
    except Exception as e:
        #print(e)
        traceback.print_exc()
        return None