import boto3
from datetime import datetime, timezone, timedelta
import os

def lambda_handler(event, context):
    # Fetch bucket name from environment variables
    bucket_name = os.environ.get('BUCKET_NAME')
    
    if not bucket_name:
        print("Error: BUCKET_NAME environment variable is not set.")
        return {
            'statusCode': 400,
            'body': 'BUCKET_NAME environment variable is missing.'
        }
        
    s3 = boto3.client('s3')
    
    # Calculate cutoff time (30 days ago)
    retention_days = 30
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=retention_days)
    
    print(f"Starting cleanup for bucket: '{bucket_name}'")
    print(f"Deleting files created before: {cutoff_time}")
    
    deleted_objects = []
    
    try:
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
