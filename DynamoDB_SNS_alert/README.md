# DynamoDB Change Event Alert Using AWS Lambda, Boto3, and SNS

## Objective
Set up an automated alert system that monitors database item changes in Amazon DynamoDB using DynamoDB Streams, parses the modifications via AWS Lambda, and sends detailed notifications via an Amazon SNS Topic to your email.

---

## Step-by-Step Instructions

### Step 1: Create and Configure the DynamoDB Table
1. Open the **AWS Management Console** and navigate to **DynamoDB**.
2. Click **Create table**.
   Example:
   - **Table name**: `CustomerReviews`
   - **Partition key**: `ReviewID` (Type: `String`)
3. Click **Create table**.
4. Once the table is active, click on it, select the **Exports and streams** tab, and find the **DynamoDB stream details** section.
5. Click **Turn on**.
6. Select **New and old images** (this sends both pre-update and post-update states to the stream) and click **Turn on stream**. Note down the **Stream ARN**.

<details open>
<summary>📸 Step 1 Screenshots (DynamoDB Table & Stream Setup)</summary>
<br>

#### Table Creation
<img src="./images/DynamoDB_CreateTable1.png" alt="Create Table 1" width="100%">
<img src="./images/DynamoDB_CreateTable2.png" alt="Create Table 2" width="100%">
<img src="./images/DynamoDB_CreateTable3.png" alt="Create Table 3" width="100%">

#### Enable DynamoDB Stream
<img src="./images/DynamoDB_ExportStream1.png" alt="Export Stream 1" width="100%">
<img src="./images/DynamoDB_ExportStream2.png" alt="Export Stream 2" width="100%">
<img src="./images/DynamoDB_ExportStream3.png" alt="Export Stream 3" width="100%">

</details>

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

<details open>
<summary>📸 Step 2 Screenshots (SNS Topic & Subscription)</summary>
<br>

#### SNS Topic Creation
<img src="./images/SNS_Create1.png" alt="SNS Create 1" width="100%">
<img src="./images/SNS_Create2.png" alt="SNS Create 2" width="100%">

#### Subscription Setup & Confirmation
<img src="./images/SNS_Subscription1.png" alt="SNS Subscription 1" width="100%">
<img src="./images/SNS_Subscription2.png" alt="SNS Subscription 2" width="100%">
<img src="./images/SNS_Subscription3.png" alt="SNS Subscription 3" width="100%">
<img src="./images/SNS_Subscription4.png" alt="SNS Subscription 4" width="100%">
<img src="./images/SNS_Subscription5.png" alt="SNS Subscription 5" width="100%">
<img src="./images/SNS_Subscription6.png" alt="SNS Subscription 6" width="100%">

</details>

---

### Step 3: Create the IAM Role for Lambda
1. Navigate to the **IAM Console**.
2. Select **Roles** -> **Create role**.
3. Choose **AWS service** -> **Lambda** trust use case. Click **Next**.
4. Create a policy with the following permissions (or attach `AmazonSNSFullAccess` and `AmazonDynamoDBFullAccess` if possible, for simplicity):
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
5. Name the role `LambdaDynamoDBSNSRole` or similar and click **Create role**.

<details open>
<summary>📸 Step 3 Screenshots (IAM Role for Lambda)</summary>
<br>

#### Role & Custom Policy Configuration
<img src="./images/IAMRole1.png" alt="IAM Role 1" width="100%">
<img src="./images/IAMRole2.png" alt="IAM Role 2" width="100%">
<img src="./images/IAMRole3.png" alt="IAM Role 3" width="100%">
<img src="./images/IAMRole4.png" alt="IAM Role 4" width="100%">
<img src="./images/IAMRole5.png" alt="IAM Role 5" width="100%">
<img src="./images/IAMRole6.png" alt="IAM Role 6" width="100%">
<img src="./images/IAMRole7.png" alt="IAM Role 7" width="100%">
<img src="./images/IAMRole8.png" alt="IAM Role 8" width="100%">

</details>

---

### Step 4: Create and Trigger the Lambda Function
1. Navigate to the **Lambda Console** and click **Create function**.
2. Configure settings:
   Example:
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

<details open>
<summary>📸 Step 4 Screenshots (Lambda Function & Trigger Configuration)</summary>
<br>

#### Lambda Creation & Env Variables
<img src="./images/Lambda1.png" alt="Lambda 1" width="100%">
<img src="./images/Lambda2.png" alt="Lambda 2" width="100%">
<img src="./images/Lambda3.png" alt="Lambda 3" width="100%">
<img src="./images/Lambda4.png" alt="Lambda 4" width="100%">
<img src="./images/Lambda5.png" alt="Lambda 5" width="100%">
<img src="./images/Lambda6.png" alt="Lambda 6" width="100%">
<img src="./images/Lambda7.png" alt="Lambda 7" width="100%">
<img src="./images/Lambda8.png" alt="Lambda 8" width="100%">

</details>

---

### Step 5: Test and Verify
1. Go to the **DynamoDB Console** -> **Explore items** -> select table `CustomerReviews`.
2. Click **Create item**:
   Example:
   - Set `ReviewID` to `101`
   - Click **Add new attribute** -> **String** (Name: `CustomerName`, Value: `Dynamo Delivery Services`)
   - Click **Add new attribute** -> **String** (Name: `ReviewText`, Value: `Excellent service!`)
   - Click **Create item**.
3. Now, select the item `101`, click **Actions** -> **Edit item**:
   - Change `ReviewText` to `Excellent service and fast delivery!`
   - Click **Save changes**.
4. Check your email inbox. You should receive:
   - An email for the `INSERT` action detailing Dynamo Delivery Services review.
   - An email for the `MODIFY` action showing the old text vs. new text.

<details open>
<summary>📸 Step 5 Screenshots (Testing & Verification)</summary>
<br>

#### DynamoDB Operations
<img src="./images/DynamoDB_CreateItem1.png" alt="Create Item 1" width="100%">
<img src="./images/DynamoDB_CreateItem2.png" alt="Create Item 2" width="100%">
<img src="./images/DynamoDB_CreateItem3.png" alt="Create Item 3" width="100%">
<img src="./images/DynamoDB_CreateItem4.png" alt="Create Item 4" width="100%">

#### Lambda Execution Verification (Logs & Triggers)
<img src="./images/LambdaExecution1.png" alt="Lambda Execution 1" width="100%">
<img src="./images/LambdaExecution2.png" alt="Lambda Execution 2" width="100%">
<img src="./images/LambdaExecution3.png" alt="Lambda Execution 3" width="100%">
<img src="./images/LambdaExecution4.png" alt="Lambda Execution 4" width="100%">

#### Email Alerts Received
<img src="./images/Email_alert1.png" alt="Email Alert 1" width="100%">
<img src="./images/Email_alert2.png" alt="Email Alert 2" width="100%">
<img src="./images/Email_alert3.png" alt="Email Alert 3" width="100%">

</details>

---

## Screenshot Gallery Summary
All step-by-step screenshots are embedded inside each respective section above. You can expand the dropdown panels under each step to see:
- **Step 1**: Table creation and turning on DynamoDB Streams.
- **Step 2**: Creating the SNS Topic and verifying subscription.
- **Step 3**: Creating the IAM Role and setting up Boto3/SNS policy access.
- **Step 4**: Writing, deploying the Lambda code, and adding the DynamoDB Stream trigger.
- **Step 5**: Inserting/modifying DynamoDB items, reviewing logs, and checking received email notifications.
