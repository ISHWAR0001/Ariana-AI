FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install system dependencies (Including PyAudio dependencies)
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    x11-xserver-utils \
    xauth \
    xvfb \
    dbus \
    dbus-x11 \
    libglib2.0-dev \
    gir1.2-gtk-3.0 \
    gir1.2-gdkpixbuf-2.0 \
    python3-gi \
    python3-gi-cairo \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-alsa \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    gstreamer1.0-pulseaudio \
    alsa-utils \
    mesa-utils \
    libgtk-3-dev \
    portaudio19-dev \
    libasound2-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*  # Cleanup to reduce image size

# Upgrade pip before installing requirements
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for X display
ENV DISPLAY=:99
ENV PULSE_SERVER=unix:/run/pulse/native

# Copy and set entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
CMD ["/entrypoint.sh"]
