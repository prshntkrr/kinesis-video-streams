#!/bin/bash
set -e

# Default values for environment variables
STREAM_NAME=${STREAM_NAME:-default-stream-name}

# Run gst-launch-1.0 with dynamic parameters
gst-inspect-1.0 kvssink
gst-launch-1.0 -v rtspsrc location="rtsp://admin:admin@192.168.0.100:1935" ! rtph264depay ! h264parse ! kvssink stream-name="${STREAM_NAME}" storage-size=128 aws-region="" access-key="" secret-key="" session-token=""
