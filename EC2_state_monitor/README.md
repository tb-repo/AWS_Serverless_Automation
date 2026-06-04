# Monitor EC2 Instance State Changes Using AWS Lambda, Boto3, and SNS

## Objective
Automatically monitor EC2 instance state transitions (such as starting, stopping, or terminating) using Amazon EventBridge, parse the state changes in AWS Lambda, and dispatch email alerts via Amazon SNS.

---

## Step-by-Step Instructions

### Step 1: Set Up an EC2 Instance
1. Open the **AWS Management Console** and navigate to **EC2**.
2. If you do not have any running or stopped instances, launch a new free-tier instance (e.g., `t2.micro` running Amazon Linux).
3. Keep it running or stopped. Note down the **Instance ID** (e.g., `i-0abcdef123456789f`).

---

### Step 2: Create or Reuse the SNS Topic
1. Navigate to the **SNS Console**.
2. Select **Topics** -> Create a standard topic (e.g., `EC2StateAlertTopic`) or reuse an existing one.
3. Ensure your email is subscribed and status is **Confirmed**.

---

### Step 3: Create the IAM Role for Lambda
1. Navigate to the **IAM Console** -> **Roles** -> **Create role**.
2. Select **AWS service** -> **Lambda** as the trusted use case. Click **Next**.
3. Create or attach a policy granting:
   - `sns:Publish`
   - CloudWatch Logs write access (`logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`).
4. Name the role `LambdaEC2SNSRole` and click **Create role**.

---

### Step 4: Create the AWS Lambda Function
1. Navigate to the **Lambda Console** and click **Create function**.
2. Configure settings:
   - **Function name**: `EC2StateMonitor`
   - **Runtime**: `Python 3.x` (e.g., Python 3.13)
   - **Execution role**: Choose **Use an existing role** and select `LambdaEC2SNSRole`.
3. Click **Create function**.
4. Paste the code from [lambda_function.py](./lambda_function.py) into the code editor and click **Deploy**.
5. Navigate to the **Configuration** tab -> **Environment variables**, click **Edit**, and add:
   - **Key**: `SNS_TOPIC_ARN`
   - **Value**: Your actual SNS Topic ARN.
6. Click **Save**.

---

### Step 5: Configure the EventBridge Rule
1. Open the **Amazon EventBridge Console**.
2. In the left sidebar, click **Rules** -> **Create rule**.
3. Configure the rule details:
   - **Name**: `EC2InstanceStateChangeRule`
   - **Event bus**: `default`
   - **Rule type**: `Rule with an event pattern`
   - Click **Next**.
4. Define the event pattern:
   - **Event source**: `AWS services`
   - **AWS service**: `EC2`
   - **Event type**: `EC2 Instance State-change Notification`
   - **State**: Check `Any state` (or select specific ones like `running` and `stopped` for targeted notifications).
   - Click **Next**.
5. Define the target:
   - **Target type**: `AWS service`
   - **Select a target**: `Lambda function`
   - **Function**: `EC2StateMonitor`
6. Click **Next**, review the configuration, and click **Create rule**.

---

### Step 6: Test and Verify
1. Go to the **EC2 Console** -> **Instances**.
2. Select your test EC2 instance.
3. Click **Instance state** -> **Stop** (if it was running) or **Start** (if it was stopped).
4. Wait 1-2 minutes for the transition to complete.
5. Check your email inbox. You should receive a formatted message detailing:
   - The instance ID.
   - The new state of the instance.
   - The time of the state transition.
6. Verify the execution prints by checking your Lambda's logs in **CloudWatch**.

---

## Example Screenshots

1. **`01_ec2_instances.png`**: The EC2 console showing your test instance and its current state.
2. **`02_eventbridge_rule_active.png`**: The EventBridge console showing your rule configured with EC2 state change pattern and Lambda target.
3. **`03_lambda_trigger_eventbridge.png`**: The Lambda overview console displaying EventBridge as the trigger source.
4. **`04_state_email_received.png`**: The email notification in your inbox showing instance state changes (e.g., `STOPPED` or `RUNNING`).
5. **`05_cloudwatch_state_logs.png`**: The CloudWatch Logs panel showing successful receipt and processing of the event payload.
