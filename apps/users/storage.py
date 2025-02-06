from storages.backends.s3boto3 import S3Boto3Storage

class S3MediaStorage(S3Boto3Storage):
    """Custom storage class for media files"""
    bucket_name = 'airvistaj'  # Replace with your bucket name
    location = 'media/'  # Directory inside the bucket for profile pictures
    file_overwrite = False  # Prevents file overwriting
    custom_domain = '%s.s3.amazonaws.com' % bucket_name  # Custom domain for media files

    def __init__(self, *args, **kwargs):
        super(S3MediaStorage, self).__init__(*args, **kwargs)
