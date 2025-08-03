"""
Station API endpoints for autocomplete functionality
"""

from flask import Blueprint, request, jsonify
from app.services import TrainService
from app import cache
import json

stations_api = Blueprint('stations_api', __name__, url_prefix='/api')

# Common Indian railway stations for quick suggestions
POPULAR_STATIONS = [
    {"name": "NEW DELHI", "code": "NDLS"},
    {"name": "MUMBAI CENTRAL", "code": "MMCT"},
    {"name": "CHENNAI CENTRAL", "code": "MAS"},
    {"name": "KOLKATA", "code": "KOAA"},
    {"name": "BANGALORE CITY", "code": "SBC"},
    {"name": "HYDERABAD DECAN", "code": "HYB"},
    {"name": "PUNE JN", "code": "PUNE"},
    {"name": "AHMEDABAD JN", "code": "ADI"},
    {"name": "JAIPUR", "code": "JP"},
    {"name": "LUCKNOW NR", "code": "LJN"},
    {"name": "KANPUR CENTRAL", "code": "CNB"},
    {"name": "NAGPUR", "code": "NGP"},
    {"name": "BHOPAL JN", "code": "BPL"},
    {"name": "INDORE JN BG", "code": "INDB"},
    {"name": "COIMBATORE JN", "code": "CBE"},
    {"name": "VIJAYAWADA JN", "code": "BZA"},
    {"name": "VISAKHAPATNAM", "code": "VSKP"},
    {"name": "THIRUVANANTHAPURAM CENTRAL", "code": "TVC"},
    {"name": "KOCHI", "code": "ERS"},
    {"name": "GUWAHATI", "code": "GHY"},
    {"name": "PATNA JN", "code": "PNBE"},
    {"name": "RANCHI", "code": "RNC"},
    {"name": "BHUBANESWAR", "code": "BBS"},
    {"name": "RAIPUR JN", "code": "R"},
    {"name": "JODHPUR JN", "code": "JU"},
    {"name": "UDAIPUR CITY", "code": "UDZ"},
    {"name": "JAMMU TAWI", "code": "JAT"},
    {"name": "AMRITSAR JN", "code": "ASR"},
    {"name": "CHANDIGARH", "code": "CDG"},
    {"name": "DEHRADUN", "code": "DDN"},
    {"name": "HARIDWAR JN", "code": "HW"},
    {"name": "VARANASI JN", "code": "BSB"},
    {"name": "ALLAHABAD JN", "code": "ALD"},
    {"name": "AGRA CANTT", "code": "AGC"},
    {"name": "GWALIOR", "code": "GWL"},
    {"name": "JABALPUR", "code": "JBP"},
    {"name": "RATLAM JN", "code": "RTM"},
    {"name": "UJJAIN JN", "code": "UJN"},
    {"name": "SURAT", "code": "ST"},
    {"name": "VADODARA JN", "code": "BRC"},
    {"name": "RAJKOT JN", "code": "RJT"},
    {"name": "BHAVNAGAR TERM", "code": "BVC"},
    {"name": "MADURAI JN", "code": "MDU"},
    {"name": "TIRUCHIRAPALLI", "code": "TPJ"},
    {"name": "SALEM JN", "code": "SA"},
    {"name": "ERODE JN", "code": "ED"},
    {"name": "TIRUNELVELI", "code": "TEN"},
    {"name": "MANGALORE CENTRAL", "code": "MAQ"},
    {"name": "MYSORE JN", "code": "MYS"},
    {"name": "HUBLI JN", "code": "UBL"},
    {"name": "BELGAUM", "code": "BGM"},
    {"name": "SOLAPUR JN", "code": "SUR"},
    {"name": "AURANGABAD", "code": "AWB"},
    {"name": "NASHIK ROAD", "code": "NK"},
    {"name": "KOLHAPUR", "code": "KOP"},
    {"name": "PANVEL", "code": "PNVL"},
    {"name": "THANE", "code": "TNA"},
    {"name": "KALYAN JN", "code": "KYN"},
    {"name": "LOKMANYA TILAK T", "code": "LTT"},
    {"name": "DADAR", "code": "DR"},
    {"name": "ANDHERI", "code": "ADH"},
    {"name": "BORIVALI", "code": "BVI"},
    {"name": "VASAI ROAD", "code": "BSR"},
    {"name": "VIRAR", "code": "VR"},
    {"name": "DOMBIVLI", "code": "DI"},
    {"name": "AMBERNATH", "code": "ABH"},
    {"name": "BADLAPUR", "code": "BDP"},
    {"name": "KARJAT", "code": "KJT"},
    {"name": "KHOPOLI", "code": "KHO"},
    {"name": "LONAVALA", "code": "LNL"},
    {"name": "KHANDALA", "code": "KAD"},
    {"name": "TALEGAON", "code": "TGN"},
    {"name": "CHINCHWAD", "code": "CCH"},
    {"name": "PIMPRI", "code": "PPR"},
    {"name": "AKURDI", "code": "AKD"},
    {"name": "DEHU ROAD", "code": "DHR"},
    {"name": "TALEGAON DABHADE", "code": "TGN"},
    {"name": "WADGAON", "code": "WDG"},
    {"name": "URULI KANCHAN", "code": "URLI"},
    {"name": "HADAPSAR", "code": "HDP"},
    {"name": "MUNDHWA", "code": "MNDW"},
    {"name": "KHARADI", "code": "KHRD"},
    {"name": "WAGHOLI", "code": "WGHL"},
    {"name": "LOHEGAON", "code": "LHG"},
    {"name": "VIMAN NAGAR", "code": "VMN"},
    {"name": "YERAWADA", "code": "YRD"},
    {"name": "KALYANI NAGAR", "code": "KLN"},
    {"name": "KOREGAON PARK", "code": "KGP"},
    {"name": "CAMP", "code": "CMP"},
    {"name": "PUNE CANTONMENT", "code": "PNCT"},
    {"name": "KHADKI", "code": "KDK"},
    {"name": "DAPODI", "code": "DPD"},
    {"name": "KASARWADI", "code": "KSW"},
    {"name": "PHUGEWADI", "code": "PHW"},
    {"name": "THERGAON", "code": "TGN"},
    {"name": "WAKAD", "code": "WKD"},
    {"name": "HINJAWADI", "code": "HJD"},
    {"name": "BALEWADI", "code": "BWD"},
    {"name": "BANER", "code": "BNR"},
    {"name": "AUNDH", "code": "AND"},
    {"name": "PASHAN", "code": "PSN"},
    {"name": "BAVDHAN", "code": "BVD"},
    {"name": "WARJE", "code": "WRJ"},
    {"name": "KARVE NAGAR", "code": "KVN"},
    {"name": "KOTHRUD", "code": "KTD"},
    {"name": "ERANDWANE", "code": "ERD"},
    {"name": "SHIVAJINAGAR", "code": "SJN"},
    {"name": "DECCAN", "code": "DCC"},
    {"name": "PUNE JN", "code": "PUNE"}
]

@stations_api.route('/stations/search')
@cache.cached(timeout=3600, query_string=True)  # Cache for 1 hour
def search_stations():
    """Search stations by name or code"""
    try:
        query = request.args.get('q', '').strip().upper()
        limit = min(int(request.args.get('limit', 10)), 20)  # Max 20 results
        
        if len(query) < 2:
            # Return popular stations for short queries
            return jsonify({
                'status': 'success',
                'stations': POPULAR_STATIONS[:limit],
                'total': len(POPULAR_STATIONS[:limit])
            })
        
        # Search in popular stations first
        matching_stations = []
        
        # Exact matches first
        for station in POPULAR_STATIONS:
            if (query in station['name'] or 
                query in station['code'] or
                station['name'].startswith(query) or
                station['code'].startswith(query)):
                matching_stations.append(station)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_stations = []
        for station in matching_stations:
            station_key = f"{station['name']}_{station['code']}"
            if station_key not in seen:
                seen.add(station_key)
                unique_stations.append(station)
        
        # Try to get more results from database if needed
        if len(unique_stations) < limit:
            try:
                db_stations = TrainService.search_stations_by_name(query)
                for code in db_stations[:limit - len(unique_stations)]:
                    if code not in [s['code'] for s in unique_stations]:
                        unique_stations.append({
                            'name': code,  # We might not have the full name
                            'code': code
                        })
            except Exception as e:
                #print(f"Database search error: {e}")
                ...
        
        return jsonify({
            'status': 'success',
            'stations': unique_stations[:limit],
            'total': len(unique_stations[:limit])
        })
        
    except Exception as e:
        #print(f"Error in station search: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to search stations',
            'stations': POPULAR_STATIONS[:10]  # Fallback to popular stations
        }), 500

@stations_api.route('/stations/popular')
@cache.cached(timeout=86400)  # Cache for 24 hours
def get_popular_stations():
    """Get list of popular stations"""
    try:
        limit = min(int(request.args.get('limit', 20)), 50)
        return jsonify({
            'status': 'success',
            'stations': POPULAR_STATIONS[:limit],
            'total': len(POPULAR_STATIONS[:limit])
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get popular stations'
        }), 500

@stations_api.route('/health')
def api_health():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': '2024-01-01T00:00:00Z',
        'version': '1.0.0'
    })