from pathlib import Path
import sys
import boto3

# Get the absolute path of the current file (only works in .py files) - path to this file ./settings.py
file_path = Path(__file__).resolve()

# Get the parent directory of the current file (main file: /yolov8-streamlit)
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there : allows for things like helper.process_license_plate()
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the main folder (basically IMAGES_DIR = ../yolov8-streamlit/'images')
ROOT = root_path.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
VIDEO = 'Video'

SOURCES_LIST = [IMAGE, VIDEO]

# S3 Videos config
s3_bucket = 'newdataa'
s3_client = boto3.client('s3')
s3_images_prefix = 'images/'
s3_videos_prefix = 'videos/'


# Images config
#IMAGES_DIR = ROOT / 'images'
#DEFAULT_IMAGE = IMAGES_DIR / 'A2C1.png'
#DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'A2C1_detected.jpg'

# Fetch the list of images from the S3 bucket
s3_images = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_images_prefix)

S3_IMAGES_DICT = {}
if 'Contents' in s3_images:
    for obj in s3_images['Contents']:
        key = obj['Key']
        if key.endswith(('jpg', 'jpeg', 'png', 'bmp', 'webp')):
            image_name = Path(key).stem
            S3_IMAGES_DICT[image_name] = f"s3://{s3_bucket}/{key}"

IMAGES_DICT = {
    **S3_IMAGES_DICT  # Include only S3 images in the dictionary
}

# Fetch the list of videos from the S3 bucket
s3_videos = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_videos_prefix)

S3_VIDEOS_DICT = {}
if 'Contents' in s3_videos:
    for obj in s3_videos['Contents']:
        key = obj['Key']
        if key.endswith(('mp4', 'avi', 'mov')):
            video_name = Path(key).stem
            S3_VIDEOS_DICT[video_name] = f"s3://{s3_bucket}/{key}"

VIDEOS_DICT = {
    **S3_VIDEOS_DICT  # Include only S3 videos in the dictionary
}

# ML Model config
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'best.pt'
DETECTION_MODEL_S = MODEL_DIR / 'best_S.pt'
