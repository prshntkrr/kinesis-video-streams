import boto3
import subprocess
import time
from datetime import datetime, timedelta

def create_hls_url(max_retries=600, delay=1):
    # Set AWS credentials and Kinesis Video Stream configuration
    STREAM_NAME = 'kinesis-video-stream'
    aws_region = 'us-east-2'

    kvs = boto3.client("kinesisvideo", region_name=aws_region)

    endpoint = kvs.get_data_endpoint(
        APIName="GET_HLS_STREAMING_SESSION_URL",
        StreamName=STREAM_NAME
    )['DataEndpoint']

    end_time = datetime.utcnow() - timedelta(hours=0)
    start_time = end_time - timedelta(hours=2)
    kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint, region_name=aws_region)

    attempts = 0
    while attempts < max_retries:
        try:
            url = kvam.get_hls_streaming_session_url(
                StreamName=STREAM_NAME,
                PlaybackMode="ON_DEMAND",
                HLSFragmentSelector={
                    'FragmentSelectorType': 'SERVER_TIMESTAMP',
                    'TimestampRange': {
                    'StartTimestamp': start_time,
                    'EndTimestamp': end_time
                    }
                }
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


def download_live_stream(hls_url, output_file):
    # Use ffmpeg to continuously download the HLS stream and save it to the output file
    cmd = [
        'ffmpeg', '-y', '-i', hls_url, '-c', 'copy',
        '-bsf:a', 'aac_adtstoasc', '-f', 'segment', '-segment_time', '2',
        '-segment_format', 'mp4', f'{output_file}_%03d.mp4'
    ]
    subprocess.run(cmd)


def main():
    output_file = 'videos'

    url = create_hls_url()
    if url:
        print(f"HLS URL: {url}")
        download_live_stream(url, output_file)
        # download_frames(url, output_file)
    else:
        print("Failed to retrieve HLS URL.")


# if __name__ == "__main__":
    main()