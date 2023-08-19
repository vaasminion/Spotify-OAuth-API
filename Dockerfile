# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables (modify these as needed)
ENV FLASK_APP=Spotify_OAuth_API.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV CLIENT_ID=
ENV CLIENT_SECRET=
ENV SCOPE=

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Expose the port that the application will run on
EXPOSE 5000


# Start Gunicorn to run the Flask application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "Spotify_OAuth_API:app"]
