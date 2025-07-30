"""
Train Views - Train search and status
"""

from flask import Blueprint, render_template, request, jsonify
from app.services import TrainService
from scripts.runningstatus import main as running_status
from scripts.railyatri import main as railyatri_status
from scripts.map import main as map_main
import concurrent.futures
from datetime import datetime
from uuid import uuid1
import traceback

trains_bp = Blueprint('trains', __name__)

@trains_bp.route('/find_trains', methods=['POST', 'GET'])
@trains_bp.route('/submitsearch', methods=['POST', 'GET'])
def submit_search():
    """Search for trains between stations"""
    try:
        if request.path.startswith('/trains/find_trains'):
            toDest = request.form.get('toDest')
            fromDest = request.form.get('fromDest')
            date = request.form.get('toDate')
        else:
            data_json = request.json
            toDest = request.json['toDest']
            fromDest = request.json['fromDest']
            date = request.json['toDate']

        # Query the database to find station codes
        to_document = TrainService.search_stations_by_name(toDest)
        from_document = TrainService.search_stations_by_name(fromDest)

        if not to_document or not from_document:
            raise ValueError("Invalid station names provided")

        to_id = to_document[0] if to_document else toDest
        from_id = from_document[0] if from_document else fromDest

        print(toDest, fromDest)
        request_id = str(uuid1())

        # Retrieve train data
        data = TrainService.get_train_data(from_id, to_id)

        if data is None:
            if not date:
                date = datetime.now().date()
            data = TrainService.fetch_trains_from_api(from_id, to_id, date)
            
            if data:
                # Save data to database
                TrainService.store_train_data(data, request_id)
                TrainService.store_keyword_search(from_id, to_id, request_id)
                
        print(f'From Station ID: {from_id}, To Station ID: {to_id}')
        print(f'Data: {data}')

        if request.path.startswith('/trains/find_trains'):
            return render_template('train_finder.html', data=data, fromDest=fromDest, toDest=toDest)
        return jsonify(data)

    except ValueError as ve:
        print(ve)
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500

@trains_bp.route('/train_finder/')
def search_train_no():
    """Get detailed train information"""
    train_no = request.args.get('train_no')
    fromDest = request.args.get('start_from')
    toDest = request.args.get('end_from')

    def fetch_map(train_no):
        return map_main(train_no)

    def fetch_running_status(train_no):
        return running_status(train_number=train_no, date=datetime.now().date())
    
    def fetch_time_table(train_no):
        return railyatri_status(train_no)
    
    # Create threads to fetch data concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        running_train_data = executor.submit(fetch_running_status, train_no)
        map_data = executor.submit(fetch_map, train_no)

    # Wait for threads to finish and get results
    map_result = map_data.result()
    status_result = running_train_data.result()
    
    return render_template('running_status.html', 
                         running_status=status_result, 
                         train_no=train_no, 
                         map=map_result,
                         fromDest=fromDest, 
                         toDest=toDest)

@trains_bp.route('/book_food/')
def book_food():
    """Food booking page"""
    train_no = request.args.get('train_no')
    fromDest = request.args.get('start_from')
    toDest = request.args.get('end_from')
    
    time_table_data = railyatri_status(train_no)
      
    return render_template('food_booking.html', 
                         train_no=train_no,
                         time_table=time_table_data,
                         fromDest=fromDest, 
                         toDest=toDest)

@trains_bp.route('/m/link-food-in-train')
def link_food_in_train():
    """Link food in train"""
    station_code = request.args.get('station_code')
    train = request.args.get('train')
    return f"Linking food in train for station {station_code} and train {train}" 