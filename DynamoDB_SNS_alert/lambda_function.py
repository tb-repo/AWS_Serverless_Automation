import boto3
import os
import json
from boto3.dynamodb.types import TypeDeserializer

# Initialize boto3 clients
sns = boto3.client('sns')
deserializer = TypeDeserializer()

def deserialize_image(image_dict):
    """Helper to convert DynamoDB stream images into standard Python dicts."""
    if not image_dict:
        return {}
    return {k: deserializer.deserialize(v) for k, v in image_dict.items()}

def lambda_handler(event, context):
    # Retrieve SNS Topic ARN from environment variables
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    
    if not sns_topic_arn:
        print("Error: SNS_TOPIC_ARN environment variable is not set.")
        return {
            'statusCode': 400,
            'body': 'SNS_TOPIC_ARN environment variable is missing.'
        }
        
    print(f"Processing DynamoDB Stream event with {len(event.get('Records', []))} record(s)...")
    
    notifications_sent = 0
    
    for record in event.get('Records', []):
        try:
            event_name = record.get('eventName')  # INSERT, MODIFY, or REMOVE
            table_name = record.get('eventSourceARN', '').split('/')[1]
            
            db_data = record.get('dynamodb', {})
            keys = deserialize_image(db_data.get('Keys', {}))
            old_image = deserialize_image(db_data.get('OldImage', {}))
            new_image = deserialize_image(db_data.get('NewImage', {}))
            
            # Format a readable, user-friendly alert message
            subject = f"DynamoDB Alert: Table '{table_name}' Item {event_name}d"
            
            message_body = (
                f"DynamoDB Stream Alert\n"
                f"====================================\n"
                f"Table Name : {table_name}\n"
                f"Action Type: {event_name}\n"
                f"Item Keys  : {json.dumps(keys, indent=2)}\n\n"
            )
            
            if event_name == 'INSERT':
                message_body += f"Added Item Details:\n{json.dumps(new_image, indent=2)}\n"
            elif event_name == 'MODIFY':
                message_body += (
                    f"Previous State:\n{json.dumps(old_image, indent=2)}\n\n"
                    f"Updated State:\n{json.dumps(new_image, indent=2)}\n"
                )
            elif event_name == 'REMOVE':
                message_body += f"Deleted Item Details:\n{json.dumps(old_image, indent=2)}\n"
                
            message_body += "\n===================================="
            
            # Print log statements for CloudWatch
            print(f"Publishing SNS notification for {event_name} action on keys: {keys}")
            
            # Publish to SNS
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject=subject,
                Message=message_body
            )
            notifications_sent += 1
            
        except Exception as e:
            print(f"Error processing record: {str(e)}")
            
    return {
        'statusCode': 200,
        'body': {
            'message': 'DynamoDB stream records processed successfully',
            'notifications_sent': notifications_sent
        }
    }
