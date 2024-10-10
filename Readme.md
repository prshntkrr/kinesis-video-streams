Running Amazon Kinesis Video Streams Producer SDK C++ in Docker

* This Docker setup provides an environment to build and run the Amazon Kinesis 
  Video Streams Producer SDK C++ with GStreamer support.


1. Build Docker Image:
    "docker build -t kinesis-video-streams-producer-sdk-cpp ."
    This command builds the Docker image kinesis-video-streams-producer-sdk-cpp 
    using the Dockerfile provided.

2. Run Docker Container:
    To run the Docker container and execute the gst-launch-1.0 command with dynamic parameters:
        "docker run -e STREAM_NAME="your-stream-name" kinesis-video-streams-producer-sdk-cpp"
        Replace "your-stream-name" with the actual stream name you want to use.
3. Download live and On Demand video from kinesis:
    For live video run "download_livestream.py"
    for On Demand video run "download_ondemand.py"
    for download frames run "download_frames_from_kinesis.py"

Additional Notes
    * Make sure Docker is installed and running on your system before executing these commands.
    * This setup assumes you have the necessary permissions and credentials to access your RTSP stream.
    * Adjust the RTSP URL (location) in the entrypoint.sh script (rtspsrc location="...") to match your 
      specific camera configuration.
    * if docker is not installed in your system than run "./check_docker.sh"
