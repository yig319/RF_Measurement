# Use a more specific Python image for better compatibility
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and clean up in one layer to reduce image size
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set environment variables
ENV PYTHONPATH=/app
ENV INPUT_DIR=/data/input
ENV OUTPUT_DIR=/data/output

# Create volume mount points
VOLUME ["/data/input", "/data/output"]

# Run the script when the container launches
ENTRYPOINT ["python", "/app/example_scripts_docker.py"]
CMD ["--input_folder", "/data/input", "--output_folder", "/data/output"]