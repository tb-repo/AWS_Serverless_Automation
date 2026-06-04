import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    print("Starting S3 bucket encryption audit...")
    
    try:
        # Retrieve all buckets in the AWS account
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        print(f"Found {len(buckets)} S3 bucket(s) to check.")
        
        unencrypted_buckets = []
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                # Query server-side encryption settings
                s3.get_bucket_encryption(Bucket=bucket_name)
                # If no exception, it has encryption configured
                print(f"Encrypted: '{bucket_name}'")
            except ClientError as e:
                # ServerSideEncryptionConfigurationNotFoundError means encryption is not configured
                error_code = e.response['Error']['Code']
                if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                    print(f"*** ALERT *** Unencrypted: '{bucket_name}'")
                    unencrypted_buckets.append(bucket_name)
                elif error_code == 'AccessDenied':
                    print(f"Access Denied for bucket '{bucket_name}'. Ensure IAM role has permissions.")
                else:
                    print(f"Error checking '{bucket_name}': {str(e)}")
                    
        print("\n=== Audit Summary ===")
        print(f"Total buckets audited: {len(buckets)}")
        print(f"Unencrypted buckets: {len(unencrypted_buckets)}")
        if unencrypted_buckets:
            print(f"List of unencrypted buckets: {unencrypted_buckets}")
        print("=====================")
        
        return {
            'statusCode': 200,
            'body': {
                'unencrypted_buckets': unencrypted_buckets,
                'total_buckets_audited': len(buckets)
            }
        }
        
    except Exception as e:
        print(f"Audit failed with exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Fatal Error: {str(e)}"
        }
