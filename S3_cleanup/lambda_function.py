import boto3
from datetime import datetime, timezone, timedelta
import os

def get_case_insensitive(data, keys_to_check):
    """Search for keys case-insensitively in a dictionary or dictionary-like object."""
    if not data:
        return None
    data_lower = {str(k).lower(): v for k, v in data.items()}
    for key in keys_to_check:
        lower_key = key.lower()
        if lower_key in data_lower:
            return data_lower[lower_key]
    return None

def list_all_objects(s3, bucket_name):
    """List all objects in the S3 bucket and return their keys."""
    try:
        keys = []
        paginator = s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name)
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    keys.append(obj['Key'])
        return keys
    except Exception as e:
        print(f"Error listing files in bucket '{bucket_name}': {str(e)}")
        return None

def lambda_handler(event, context):
    # Ensure event is a dictionary safely
    if not isinstance(event, dict):
        event = {}
        
    # Fetch bucket name case-insensitively
    bucket_keys = ['bucket_name', 'bucket', 'bucketname']
    bucket_name = get_case_insensitive(event, bucket_keys) or get_case_insensitive(dict(os.environ), bucket_keys)
    
    if not bucket_name:
        print("Error: Bucket name is not set in event payload or environment variables.")
        return {
            'statusCode': 400,
            'body': 'Bucket name is missing.'
        }
        
    s3 = boto3.client('s3')
    
    # Fetch retention period (in days) case-insensitively, defaulting to 30
    retention_days = 30
    retention_keys = ['retention_days', 'retention_period', 'retention', 'retentionperiod', 'retentiondays']
    retention_val = get_case_insensitive(event, retention_keys) or get_case_insensitive(dict(os.environ), retention_keys)
    
    if retention_val is not None:
        try:
            retention_days = int(retention_val)
        except ValueError:
            print(f"Warning: Invalid retention period value '{retention_val}'. Falling back to default: {retention_days} days.")
            
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=retention_days)
    
    print(f"Starting cleanup for bucket: '{bucket_name}'")
    print(f"Retention period: {retention_days} days")
    print(f"Deleting files created before: {cutoff_time}")
    
    deleted_objects = []
    
    try:
        # List files before deletion
        print("Files in bucket BEFORE cleanup:")
        initial_files = list_all_objects(s3, bucket_name)
        if initial_files is not None:
            if initial_files:
                for key in initial_files:
                    print(f"  - {key}")
            else:
                print("  (No files found)")
        
        # Paginate to handle buckets with large numbers of files
        paginator = s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name)
        
        objects_to_delete = []
        
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    last_modified = obj['LastModified']
                    key = obj['Key']
                    
                    if last_modified < cutoff_time:
                        print(f"Flagged for deletion: {key} (Modified: {last_modified})")
                        objects_to_delete.append({'Key': key})
                        deleted_objects.append(key)
                        
                        # S3 delete_objects takes up to 1000 keys at once
                        if len(objects_to_delete) == 1000:
                            s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
                            objects_to_delete = []
                            
        # Delete any remaining flagged objects
        if objects_to_delete:
            s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
            
        print(f"Cleanup complete. Total objects deleted: {len(deleted_objects)}")
        
        # List files after deletion
        print("Files in bucket AFTER cleanup:")
        remaining_files = list_all_objects(s3, bucket_name)
        if remaining_files is not None:
            if remaining_files:
                for key in remaining_files:
                    print(f"  - {key}")
            else:
                print("  (No files remaining)")
                
        return {
            'statusCode': 200,
            'body': {
                'message': 'Cleanup successful',
                'deleted_count': len(deleted_objects),
                'deleted_files': deleted_objects
            }
        }
        
    except Exception as e:
        print(f"Error during S3 cleanup: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
