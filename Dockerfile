# Use a base Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project into the container
COPY . .

# Set the environment variable to indicate the app should run in production
ENV FLASK_ENV=production

# Expose the port your app will run on (e.g., 5000 for Flask)
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "-w", "4", "app:app"]
