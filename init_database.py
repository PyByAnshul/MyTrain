#!/usr/bin/env python3
"""
Database initialization script for MyTrain application
This script creates the SQLite database and all required tables
"""

import os
import sys
from app import create_app
from sqlalchemy import inspect

def init_database():
    """Initialize the database with all tables"""
    app = create_app()
    
    try:
        with app.app_context():
            from app import db
            from app.models import UserData, SearchResult, KeywordSearch, TrainDatabase, StationsTrain, Booking
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if tables were created
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Created tables: {', '.join(tables)}")
            
            # Verify database file exists
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            if os.path.exists(db_path):
                print(f"💾 Database file created at: {db_path}")
            else:
                print(f"⚠️  Database file not found at: {db_path}")
                
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    return True

def check_database():
    """Check database status"""
    app = create_app()
    
    try:
        with app.app_context():
            from app import db
            from app.models import UserData, SearchResult, KeywordSearch, TrainDatabase, StationsTrain, Booking
            
            # Check if tables exist
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Database contains {len(tables)} tables:")
            for table in tables:
                print(f"   - {table}")
            
            # Check record counts
            user_count = UserData.query.count()
            train_count = SearchResult.query.count()
            station_count = TrainDatabase.query.count()
            booking_count = Booking.query.count()
            
            print(f"\n📈 Record counts:")
            print(f"   - Users: {user_count}")
            print(f"   - Trains: {train_count}")
            print(f"   - Stations: {station_count}")
            print(f"   - Bookings: {booking_count}")
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    print("🚂 MyTrain Database Initialization")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_database()
    else:
        success = init_database()
        if success:
            print("\n✅ Database initialization completed successfully!")
            print("You can now run the MyTrain application with: python run.py")
        else:
            print("\n❌ Database initialization failed!")
            sys.exit(1) 