# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY ./app ./app
COPY .env .

# Expose the application port
EXPOSE 8000

# Command to run the application
# CMD ["python", "-m", "app.main"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.main:app"]

