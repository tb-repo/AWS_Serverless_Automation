# Assignment 7: DynamoDB Item Change Alert Using AWS Lambda, Boto3, and SNS

## Objective
Set up an automated system that monitors database item changes in Amazon DynamoDB using DynamoDB Streams, parses the modifications via AWS Lambda, and sends detailed notifications via an Amazon SNS Topic to your email.

---

## Step-by-Step Instructions

### Step 1: Create and Configure the DynamoDB Table
1. Open the **AWS Management Console** and navigate to **DynamoDB**.
2. Click **Create table**.
   - **Table name**: `CustomerReviews`
   - **Partition key**: `ReviewID` (Type: `String`)
3. Click **Create table**.
4. Once the table is active, click on it, select the **Exports and streams** tab, and find the **DynamoDB stream details** section.
5. Click **Turn on**.
6. Select **New and old images** (this sends both pre-update and post-update states to the stream) and click **Turn on stream**. Note down the **Stream ARN**.

---

### Step 2: Create and Subscribe to the SNS Topic
1. Navigate to the **SNS Console**.
2. Select **Topics** -> **Create topic**.
3. Select type **Standard**, name it `DynamoDBItemAlerts`, and click **Create topic**. Note down the **Topic ARN**.
4. In the topic page, click **Create subscription**.
   - **Protocol**: `Email`
   - **Endpoint**: Enter your personal email address.
5. Click **Create subscription**.
6. **Important**: Open your email inbox, look for the AWS notification, and click **Confirm Subscription**.

---

### Step 3: Create the IAM Role for Lambda
1. Navigate to the **IAM Console**.
2. Select **Roles** -> **Create role**.
3. Choose **AWS service** -> **Lambda** trust use case. Click **Next**.
4. Create a policy with the following permissions (or attach `AmazonSNSFullAccess` and `AmazonDynamoDBFullAccess` for assignment simplicity):
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "sns:Publish"
               ],
               "Resource": "<your-sns-topic-arn>"
           },
           {
               "Effect": "Allow",
               "Action": [
                   "dynamodb:DescribeStream",
                   "dynamodb:GetRecords",
                   "dynamodb:GetShardIterator",
                   "dynamodb:ListStreams"
               ],
               "Resource": "<your-dynamodb-stream-arn>"
           },
           {
               "Effect": "Allow",
               "Action": [
                   "logs:CreateLogGroup",
                   "logs:CreateLogStream",
                   "logs:PutLogEvents"
               ],
               "Resource": "*"
           }
       ]
   }
   ```
5. Name the role `LambdaDynamoDBSNSRole` and click **Create role**.

---

### Step 4: Create and Trigger the Lambda Function
1. Navigate to the **Lambda Console** and click **Create function**.
2. Configure settings:
   - **Function name**: `DynamoDBStreamAlert`
   - **Runtime**: `Python 3.x` (e.g., Python 3.13)
   - **Execution role**: Choose **Use an existing role** and select `LambdaDynamoDBSNSRole`.
3. Click **Create function**.
4. In the code editor, paste the contents of [lambda_function.py](./lambda_function.py) and click **Deploy**.
5. Go to the **Configuration** tab -> **Environment variables**, click **Edit**, and add:
   - **Key**: `SNS_TOPIC_ARN`
   - **Value**: Your actual SNS Topic ARN from Step 2.
6. In the **Function overview** block, click **Add trigger**.
   - Select **DynamoDB** from the dropdown.
   - Choose the DynamoDB table `CustomerReviews`.
   - Set **Batch size** to `1`.
   - Set **Starting position** to `Latest`.
   - Click **Add**.

---

### Step 5: Test and Verify
1. Go to the **DynamoDB Console** -> **Explore items** -> select table `CustomerReviews`.
2. Click **Create item**:
   - Set `ReviewID` to `101`
   - Click **Add new attribute** -> **String** (Name: `CustomerName`, Value: `Alice`)
   - Click **Add new attribute** -> **String** (Name: `ReviewText`, Value: `Excellent service!`)
   - Click **Create item**.
3. Now, select the item `101`, click **Actions** -> **Edit item**:
   - Change `ReviewText` to `Excellent service and fast delivery!`
   - Click **Save changes**.
4. Check your email inbox. You should receive:
   - An email for the `INSERT` action detailing Alice's review.
   - An email for the `MODIFY` action showing the old text vs. new text.

---

## Example Screenshots

1. **`01_dynamodb_stream_enabled.png`**: The DynamoDB console showing that Streams are active with "New and old images".
2. **`02_sns_subscription_confirmed.png`**: The SNS console showing your email subscription status as `Confirmed`.
3. **`03_lambda_trigger_configured.png`**: The Lambda function overview displaying DynamoDB as the active trigger source.
4. **`04_email_alert_received.png`**: A screenshot of the formatted change-notification email in your inbox.
5. **`05_cloudwatch_stream_logs.png`**: The CloudWatch stream logs showing key deserialization and execution outputs.
