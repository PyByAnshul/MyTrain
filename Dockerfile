# Use the official Python 3.8 image
FROM python:3.8

# Set up the application
RUN mkdir /app
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Initialize SQLite database
RUN python init_database.py

# Expose port
EXPOSE 5000

# Run the services
CMD gunicorn -w 4 -b 0.0.0.0:5000 run:app
