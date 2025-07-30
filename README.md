# MyTrain - Railway Information & Booking System

A comprehensive Flask-based web application for Indian railway services including train search, booking, running status, and food ordering.

## 🏗️ Project Structure

```
MyTrain/
├── app/                          # Main application package
│   ├── __init__.py              # Application factory
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   ├── train.py            # Train-related models
│   │   └── booking.py          # Booking model
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py     # User operations
│   │   ├── train_service.py    # Train operations
│   │   ├── booking_service.py  # Booking operations
│   │   └── email_service.py    # Email operations
│   ├── views/                  # Route handlers
│   │   ├── __init__.py
│   │   ├── main.py            # Main routes
│   │   ├── auth.py            # Authentication routes
│   │   ├── trains.py          # Train routes
│   │   ├── booking.py         # Booking routes
│   │   └── errors.py          # Error handlers
│   ├── api/                   # REST API endpoints
│   │   ├── __init__.py
│   │   └── routes.py          # API routes
│   ├── static/                # Static files (CSS, JS, images)
│   └── templates/             # HTML templates
├── scripts/                   # External API integrations
├── migrations/                # Database migrations
├── tests/                     # Test files
├── config.py                  # Configuration
├── run.py                     # Application entry point
├── init_database.py           # Database initialization
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
└── docker-compose.yml         # Docker Compose configuration
```

## 🚀 Features

- **User Management**: Registration, login, and profile management
- **Train Search**: Find trains between stations with real-time data
- **Running Status**: Check live train running status
- **Ticket Booking**: Book tickets with QR code generation
- **Food Booking**: Order food on trains
- **Email Notifications**: OTP verification and booking confirmations
- **Responsive Design**: Mobile-friendly interface

## 🛠️ Technology Stack

- **Backend**: Flask, SQLAlchemy, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite with ORM
- **Email**: Flask-Mail
- **External APIs**: Indian Railways, Railyatri
- **Deployment**: Docker, Gunicorn

## 📋 Database Schema

### Tables
1. **user_data** - User registration and authentication
2. **search_result** - Cached train search results
3. **keywordsearch** - Search queries for caching
4. **traindatabase** - Station information
5. **stations_train** - Train route information
6. **bookings** - Ticket booking records

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd MyTrain
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
python init_database.py
```

### 4. Run the Application
```bash
# Development mode
python run.py

# Production mode
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 5. Docker Setup (Optional)
```bash
# Build and run with Docker
docker-compose up --build

# Or build manually
docker build -t mytrain .
docker run -p 5000:5000 mytrain
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key
- `MAIL_SERVER`: SMTP server for emails
- `MAIL_USERNAME`: Email username
- `MAIL_PASSWORD`: Email password
- `SQLALCHEMY_DATABASE_URI`: Database connection string

### Database Configuration
The application uses SQLite by default. The database file (`mytrain.db`) will be created in the project root.

## 📊 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/signupForm` - User registration
- `POST /auth/verifyOTP` - OTP verification

### Trains
- `GET /trains/find_trains` - Search trains
- `GET /trains/train_finder/` - Get train details
- `GET /trains/book_food/` - Food booking page

### Booking
- `GET /booking/book_ticket/` - Booking page
- `POST /booking/book/book_ticket` - Create booking

### API
- `POST /api/find_stations` - Search stations
- `POST /api/getData` - Get train data

## 🧪 Testing

```bash
# Run tests (when implemented)
python -m pytest tests/

# Check database status
python init_database.py check
```

## 📈 Performance Considerations

- **Caching**: Train search results are cached in the database
- **Concurrent Processing**: Multiple API calls run in parallel
- **Database Indexing**: Automatic indexes on primary keys
- **Connection Pooling**: Optimized for SQLite

## 🔒 Security Features

- **Input Validation**: All user inputs are validated
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Session Management**: Secure session handling
- **Error Handling**: Comprehensive error pages

## 🚨 Troubleshooting

### Common Issues

1. **Database Locked**
   ```bash
   # Check if another process is using the database
   lsof mytrain.db
   ```

2. **Import Errors**
   ```bash
   # Ensure you're in the correct directory
   cd /path/to/MyTrain
   ```

3. **Port Already in Use**
   ```bash
   # Change port in run.py or kill existing process
   lsof -ti:5000 | xargs kill -9
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please open an issue on GitHub.

---

**MyTrain** - Making Indian Railways accessible and user-friendly! 🚂






