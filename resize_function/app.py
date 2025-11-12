import boto3
from PIL import Image
import io
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = event['source_bucket']
    destination_bucket = event['destination_bucket']
    image_key = event['image_key']

    try:
        # Download image from S3
        response = s3.get_object(Bucket=source_bucket, Key=image_key)
        image = Image.open(response['Body'])

        # Resize to thumbnail
        image.thumbnail((128, 128))
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)

        # Upload to destination bucket
        s3.put_object(
            Bucket=destination_bucket,
            Key=f"thumb-{image_key}",
            Body=buffer,
            ContentType='image/jpeg'
        )

        return {"status": "success", "thumb_key": f"thumb-{image_key}"}
    except Exception as e:
        return {"status": "fail", "error": str(e)}
