import uuid
import boto3
from TaskMailer  import settings

def upload_to_s3(file):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)

    key = f"profile_pictures/{uuid.uuid4()}.jpg"
    s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, key)  # 🔥 Removed ExtraArgs
    return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{key}"


