from app import db
from datetime import datetime

class SearchResult(db.Model):
    __tablename__ = 'search_result'
    id = db.Column(db.Integer, primary_key=True)
    train_number = db.Column(db.String(20), nullable=False)
    train_name = db.Column(db.String(200))
    from_station = db.Column(db.String(10))
    to_station = db.Column(db.String(10))
    departure_time = db.Column(db.String(10))
    arrival_time = db.Column(db.String(10))
    duration = db.Column(db.String(20))
    running_days = db.Column(db.String(50))
    train_data = db.Column(db.Text)  # JSON string for additional data
    request_ids = db.Column(db.Text)  # JSON string of request IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class KeywordSearch(db.Model):
    __tablename__ = 'keywordsearch'
    id = db.Column(db.Integer, primary_key=True)
    toDest = db.Column(db.String(10), nullable=False)
    fromDest = db.Column(db.String(10), nullable=False)
    request_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TrainDatabase(db.Model):
    __tablename__ = 'traindatabase'
    id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(200), unique=True, nullable=False)
    station_code = db.Column(db.String(10))
    station_data = db.Column(db.Text)  # JSON string for additional data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StationsTrain(db.Model):
    __tablename__ = 'stations_train'
    id = db.Column(db.Integer, primary_key=True)
    train_no = db.Column(db.String(20), unique=True, nullable=False)
    stations = db.Column(db.Text)  # JSON string of station list
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 