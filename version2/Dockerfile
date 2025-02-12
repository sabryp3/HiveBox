# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# If there are no dependencies, this line can be removed
# RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 80

# Run version_2.py when the container launches
CMD ["python", "version_2.py"]