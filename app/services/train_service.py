"""
Train Service - Business logic for train operations
"""

from app.models import SearchResult, KeywordSearch, TrainDatabase, StationsTrain
from app import db
import json
from scripts.indiarailway import main as indiatrain
from scripts.fetch_stations import main as station_info_train_no
from datetime import datetime

class TrainService:
    """Service class for train-related operations"""
    
    @staticmethod
    def store_train_data(data, request_id):
        """Store train search results in database"""
        try:
            for train_data in data:
                # Check if train already exists
                existing_train = SearchResult.query.filter_by(
                    train_number=train_data.get('train_number')
                ).first()
                
                if existing_train:
                    # Update existing record
                    existing_train.train_name = train_data.get('train_name', '')
                    existing_train.from_station = train_data.get('from_station', '')
                    existing_train.to_station = train_data.get('to_station', '')
                    existing_train.departure_time = train_data.get('departure_time', '')
                    existing_train.arrival_time = train_data.get('arrival_time', '')
                    existing_train.duration = train_data.get('duration', '')
                    existing_train.running_days = train_data.get('running_days', '')
                    existing_train.train_data = json.dumps(train_data)
                    
                    # Add request_id to existing list
                    request_ids = json.loads(existing_train.request_ids) if existing_train.request_ids else []
                    if request_id not in request_ids:
                        request_ids.append(request_id)
                    existing_train.request_ids = json.dumps(request_ids)
                else:
                    # Create new record
                    new_train = SearchResult(
                        train_number=train_data.get('train_number', ''),
                        train_name=train_data.get('train_name', ''),
                        from_station=train_data.get('from_station', ''),
                        to_station=train_data.get('to_station', ''),
                        departure_time=train_data.get('departure_time', ''),
                        arrival_time=train_data.get('arrival_time', ''),
                        duration=train_data.get('duration', ''),
                        running_days=train_data.get('running_days', ''),
                        train_data=json.dumps(train_data),
                        request_ids=json.dumps([request_id])
                    )
                    db.session.add(new_train)
            
            db.session.commit()
            return True, {'status': 'successfully updated and upserted data in database'}
        except Exception as e:
            db.session.rollback()
            return False, {'status': f'error updating database: {e}'}
    
    @staticmethod
    def get_train_data(toDest, fromDest):
        """Get train data from database"""
        try:
            # Find request_id for this search
            keyword_search = KeywordSearch.query.filter_by(
                toDest=toDest, 
                fromDest=fromDest
            ).order_by(KeywordSearch.created_at.desc()).first()
            
            if keyword_search:
                request_id = keyword_search.request_id
                # Get all trains with this request_id
                search_results = SearchResult.query.all()
                trains = []
                
                for result in search_results:
                    if result.request_ids:
                        request_ids = json.loads(result.request_ids)
                        if request_id in request_ids:
                            train_data = json.loads(result.train_data) if result.train_data else {}
                            trains.append(train_data)
                
                return trains if trains else None
            return None
        except Exception as e:
            print(f"Error in get_train_data: {e}")
            return None
    
    @staticmethod
    def store_keyword_search(toDest, fromDest, request_id):
        """Store keyword search in database"""
        try:
            new_search = KeywordSearch(
                toDest=toDest,
                fromDest=fromDest,
                request_id=request_id
            )
            db.session.add(new_search)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
    @staticmethod
    def get_train_details(train_no):
        """Get detailed train information"""
        try:
            train = SearchResult.query.filter_by(train_number=train_no).first()
            if train and train.train_data:
                return json.loads(train.train_data)
            return None
        except Exception as e:
            print(f"Error in get_train_details: {e}")
            return None
    
    @staticmethod
    def store_station_data(new_stations):
        """Store station data in database"""
        try:
            for station in new_stations:
                existing_station = TrainDatabase.query.filter_by(
                    station_name=station['station_name']
                ).first()
                if existing_station:
                    # Update existing station
                    existing_station.station_code = station.get('station_code', '')
                    existing_station.station_data = json.dumps(station)
                else:
                    # Create new station
                    new_station = TrainDatabase(
                        station_name=station['station_name'],
                        station_code=station.get('station_code', ''),
                        station_data=json.dumps(station)
                    )
                    db.session.add(new_station)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
    @staticmethod
    def store_train_stations(train_no, stations):
        """Store train station information"""
        try:
            existing_train = StationsTrain.query.filter_by(train_no=train_no).first()
            if existing_train:
                existing_train.stations = json.dumps(stations)
            else:
                new_train_stations = StationsTrain(
                    train_no=train_no,
                    stations=json.dumps(stations)
                )
                db.session.add(new_train_stations)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
    @staticmethod
    def check_train_exists(train_no):
        """Check if train exists and return station information"""
        try:
            train_info = StationsTrain.query.filter_by(train_no=train_no).first()
            if train_info and train_info.stations:
                return json.loads(train_info.stations)
            else:
                # Fetch from external API
                stations = station_info_train_no(train_no)
                if stations and all(stations):
                    TrainService.store_train_stations(train_no, stations)
                    return stations
                else:
                    return None
        except Exception as e:
            print(f"Error in check_train_exists: {e}")
            return None
    
    @staticmethod
    def search_stations_by_name(station_name):
        """Search stations by name"""
        try:
            stations = TrainDatabase.query.filter(
                TrainDatabase.station_name.like(f'%{station_name}%')
            ).all()
            return [station.station_code for station in stations]
        except Exception as e:
            print(f"Error in search_stations_by_name: {e}")
            return []
    
    @staticmethod
    def fetch_trains_from_api(from_id, to_id, date):
        """Fetch trains from external API"""
        try:
            dic = indiatrain(from_id, to_id, date)
            data = dic.get('train_between_stations', [])
            if dic.get('status') != 200:
                data = ['no data' for _ in range(10)]
            return data
        except Exception as e:
            print(f"Error in fetch_trains_from_api: {e}")
            return [] 