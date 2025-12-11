# Use an official Python runtime as a parent image
FROM python:3.12-slim
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file into the container at /app
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application's code into the container at /app
# This includes app.py, your database, and the logo image
COPY . .
# Expose the port the app runs on
EXPOSE 8501
# Define the command to run your app
CMD ["streamlit", "run", "app.py"]
