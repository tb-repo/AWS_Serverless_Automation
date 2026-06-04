import boto3
from datetime import datetime, timedelta, timezone
import os

# Initialize boto3 clients
cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Fetch configurations from environment variables or defaults
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    load_balancer_suffix = os.environ.get('LOAD_BALANCER_SUFFIX') # e.g., app/my-alb/123456789
    
    if not sns_topic_arn or not load_balancer_suffix:
        print("Error: SNS_TOPIC_ARN and LOAD_BALANCER_SUFFIX must be configured.")
        return {
            'statusCode': 400,
            'body': 'Required environment variables are missing.'
        }
        
    threshold = float(os.environ.get('THRESHOLD', '10'))
    namespace = os.environ.get('METRIC_NAMESPACE', 'AWS/ApplicationELB')
    metric_name = os.environ.get('METRIC_NAME', 'HTTPCode_Target_5XX_Count')
    
    print(f"Auditing ELB '{load_balancer_suffix}' for metric '{metric_name}' in namespace '{namespace}'...")
    
    # Define timeframe: Last 5 minutes
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=5)
    
    try:
        # Retrieve metric statistics from CloudWatch
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=[
                {
                    'Name': 'LoadBalancer',
                    'Value': load_balancer_suffix
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,  # 5 minutes
            Statistics=['Sum']
        )
        
        datapoints = response.get('Datapoints', [])
        
        # Determine 5xx error count (default to 0.0 if no datapoints are returned)
        error_sum = 0.0
        if datapoints:
            error_sum = datapoints[0].get('Sum', 0.0)
            
        print(f"Retrieve completed. 5xx Error Sum for last 5 mins: {error_sum} (Threshold: {threshold})")
        
        # Check if the sum exceeds the configured threshold
        if error_sum > threshold:
            subject = f"CRITICAL ALERT: ELB 5xx Error Spike Detected!"
            message_body = (
                f"ELB 5xx Error Spike Alert\n"
                f"====================================\n"
                f"Load Balancer: {load_balancer_suffix}\n"
                f"Metric Name  : {metric_name}\n"
                f"Time Window  : {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')} to {end_time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
                f"Current Sum  : {error_sum} errors\n"
                f"Threshold    : {threshold} errors\n"
                f"Action       : Please investigate target group health and application logs immediately.\n"
                f"===================================="
            )
            
            print(f"Spike detected! Sending SNS notification to topic...")
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject=subject,
                Message=message_body
            )
            
            return {
                'statusCode': 200,
                'body': f"Spike detected. Alarm raised. Count: {error_sum}"
            }
            
        print("Metric is within healthy parameters. No actions taken.")
        return {
            'statusCode': 200,
            'body': f"Metric healthy. Count: {error_sum}"
        }
        
    except Exception as e:
        print(f"Failed to retrieve CloudWatch metrics or send SNS: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
