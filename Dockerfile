FROM python:3.9-slim

# Install Docker CLI and pip dependencies
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Docker Compose
RUN apt-get update && \
    apt-get install -y curl && \
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install pyyaml

# Copy the script to the image
COPY save_images.py /usr/local/bin/save_images.py

# Set the working directory
WORKDIR /data

# Set the entrypoint to the script
ENTRYPOINT ["python", "/usr/local/bin/save_images.py"]