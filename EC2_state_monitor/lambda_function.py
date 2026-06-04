import boto3
import os

# Initialize boto3 SNS client
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Fetch SNS Topic ARN from environment variables
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    
    if not sns_topic_arn:
        print("Error: SNS_TOPIC_ARN environment variable is not set.")
        return {
            'statusCode': 400,
            'body': 'SNS_TOPIC_ARN environment variable is missing.'
        }
        
    print("Received EC2 State Change event:")
    
    try:
        # Extract details from the EventBridge payload
        detail = event.get('detail', {})
        instance_id = detail.get('instance-id')
        state = detail.get('state')
        time = event.get('time')
        region = event.get('region')
        
        if not instance_id or not state:
            print("Error: Event does not contain expected EC2 state change details.")
            print(f"Event: {event}")
            return {
                'statusCode': 400,
                'body': 'Invalid event format.'
            }
            
        print(f"Alert: EC2 instance '{instance_id}' changed state to '{state}' in region '{region}' at time '{time}'")
        
        # Format the notification message
        subject = f"EC2 Instance State Alert: {instance_id} is {state.upper()}"
        
        message_body = (
            f"*** EC2 State Change Notification ***\n"
            f"====================================\n"
            f"Instance ID   : {instance_id}\n"
            f"New State     : {state.upper()}\n"
            f"Time of Event : {time}\n"
            f"AWS Region    : {region}\n"
            f"Action Taken  : Event detected by EventBridge and dispatched via SNS.\n"
            f"===================================="
        )
        
        # Publish alert to the SNS Topic
        print(f"Publishing EC2 state change alert to SNS...")
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject=subject,
            Message=message_body
        )
        
        return {
            'statusCode': 200,
            'body': f"Alert sent for instance {instance_id} status {state}."
        }
        
    except Exception as e:
        print(f"Error executing EC2 State Monitor: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
