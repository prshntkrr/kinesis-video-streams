import boto3
import subprocess
import time


def create_hls_url(max_retries=600, delay=1):
    # Set AWS credentials and Kinesis Video Stream configuration
    STREAM_NAME = 'kinesis-video-stream'
    aws_region = 'us-east-2'

    kvs = boto3.client("kinesisvideo", region_name=aws_region)

    endpoint = kvs.get_data_endpoint(
        APIName="GET_HLS_STREAMING_SESSION_URL",
        StreamName=STREAM_NAME
    )['DataEndpoint']

    kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint, region_name=aws_region)

    attempts = 0
    while attempts < max_retries:
        try:
            url = kvam.get_hls_streaming_session_url(
                StreamName=STREAM_NAME,
                PlaybackMode="LIVE"
            )['HLSStreamingSessionURL']
            return url
        except kvam.exceptions.ResourceNotFoundException:
            print("Stream not yet available, retrying...")
        except kvam.exceptions.ClientError as e:
            print(f"Client error occurred: {e}, retrying...")
        attempts += 1
        time.sleep(delay)
    print("Max retries reached. Stream is not available.")
    return None


def download_live_stream_frames(hls_url, output_dir):
    # Use ffmpeg to continuously download the HLS stream and save frames to the output directory
    cmd = [
        'ffmpeg', '-y', '-i', hls_url,
        '-vf', 'fps=16', f'{output_dir}/frame_%04d.jpg'
    ]
    subprocess.run(cmd)


def main():
    output_dir = 'live_frames'

    url = create_hls_url()
    if url:
        print(f"HLS URL: {url}")
        download_live_stream_frames(url, output_dir)
    else:
        print("Failed to retrieve HLS URL.")


if __name__ == "__main__":
    main()
