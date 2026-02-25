# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory
WORKDIR /code

# Install system dependencies (ffmpeg is required for Whisper/Gradio audio processing)
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Set up a non-root user (Required by Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Change working directory to the user's home directory
WORKDIR $HOME/app

# Copy the application code
COPY --chown=user . $HOME/app

# Expose the port Gradio runs on
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]