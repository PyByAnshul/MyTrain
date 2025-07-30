"""
API Routes - REST API endpoints
"""

from flask import Blueprint, request, jsonify
from app.services import TrainService
import requests
import random

api_bp = Blueprint('api', __name__)

@api_bp.route('/find_stations', methods=['POST'])
def find_stations():
    """Find stations by name"""
    station_name = request.json.get('station_name')
    print(station_name)
    try:
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.7',
            'origin': 'https://www.railyatri.in',
            'priority': 'u=1, i',
            'referer': 'https://www.railyatri.in/',
            '^sec-ch-ua': '^\\^Brave^\\^;v=^\\^125^\\^, ^\\^Chromium^\\^;v=^\\^125^\\^, ^\\^Not.A/Brand^\\^;v=^\\^24^\\^^',
            'sec-ch-ua-mobile': '?0',
            '^sec-ch-ua-platform': '^\\^Windows^\\^^',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }

        params = (
            ('q', station_name),
            ('hide_city', 'true'),
        )

        response = requests.get('https://api.railyatri.in/api/common_city_station_search.json', 
                              headers=headers, params=params)
        stations = response.json().get('items')
        station_names = [station['station_name'] for station in stations]
        
        # Store station data
        TrainService.store_station_data(stations)
    
    except Exception as e:
        print(f"Error fetching stations: {e}")
        # Fallback to stored stations
        from static.stationdata import stations as stations_stored
        station_names = stations_stored.suggestions
    print(station_names)
    return jsonify(station_names)

@api_bp.route('/getData', methods=['POST'])
def get_data():
    """Get train data for display"""
    request_data = request.json
    current_url = request_data.get('train_no')
    train_no = current_url[current_url.find('=')+1:current_url.find('&'):]
    
    # Check if station info for train_no exists
    station_info = TrainService.check_train_exists(train_no)
    
    if station_info:
        random_stations = random.sample(station_info, 2)
        html_text = f"{random_stations[0]} ●---🚂---● {random_stations[1]}"
    else:
        html_text = "Station information not available"
    
    return jsonify(html_text) 