#!/bin/sh

# Start D-Bus service
dbus-daemon --system --fork

# Start Xvfb in the background
Xvfb :99 -screen 0 1920x1080x24 &
sleep 5  # Give Xvfb enough time to initialize

# Export DISPLAY variable
export DISPLAY=:99
export XAUTHORITY=/root/.Xauthority

# Create an empty .Xauthority file and generate auth data
touch /root/.Xauthority
xauth generate :99 . trusted

# Start PulseAudio in user mode (not system mode)
mkdir -p /root/.config/pulse
echo "daemonize = yes" > /root/.config/pulse/client.conf
pulseaudio --start --log-target=syslog
sleep 2  # Ensure PulseAudio is ready

# Debugging: Check if `gi` is installed
python3 -c "import gi" 2>/dev/null || echo "Error: Python GObject Introspection (gi) module is missing!"

# Start the Python application
exec python3 main.py
