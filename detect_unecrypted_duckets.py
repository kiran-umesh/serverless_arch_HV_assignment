import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):
    detect_unencrypted_buckets()

def list_all_buckets():
    try:
        response = s3.list_buckets()
        return response['Buckets']
    except ClientError as e:
        print(f"Error listing buckets: {e}")
        return []

def check_bucket_encryption(bucket_name):
    try:
        response = s3.get_bucket_encryption(Bucket=bucket_name)
        encryption = response['ServerSideEncryptionConfiguration']
        return True  # Bucket is encrypted
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
            return False  # Bucket is not encrypted
        else:
            print(f"Error checking encryption for bucket {bucket_name}: {e}")
            return None  # Error occurred

def detect_unencrypted_buckets():
    buckets = list_all_buckets()
    if not buckets:
        print("No buckets found or error in listing buckets.")
        return
    
    unencrypted_buckets = []

    for bucket in buckets:
        bucket_name = bucket['Name']
        is_encrypted = check_bucket_encryption(bucket_name)

        if is_encrypted is False:
            print(f"Bucket without encryption: {bucket_name}")
            unencrypted_buckets.append(bucket_name)
        elif is_encrypted is None:
            print(f"Skipping bucket {bucket_name} due to an error.")

    if unencrypted_buckets:
        print(f"Unencrypted buckets: {unencrypted_buckets}")
    else:
        print("All buckets have server-side encryption enabled.")
