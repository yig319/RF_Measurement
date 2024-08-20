# Use a more comprehensive Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

ENV PYTHONPATH=/app

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Set default values for input and output directories
ENV INPUT_DIR=/app/input
ENV OUTPUT_DIR=/app/output

# Run the script when the container launches
CMD python /app/example_scripts_docker.py $INPUT_DIR $OUTPUT_DIR