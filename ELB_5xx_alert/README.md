# Monitor and Alert ELB 5xx Errors Using AWS Lambda, Boto3, and SNS

## Objective
Set up an automated system that checks the CloudWatch metrics of an Elastic Load Balancer (ELB) every 5 minutes and sends an immediate email alert via SNS if the number of 5xx errors exceeds a specified threshold.

---

## Step-by-Step Instructions

### Step 1: Identify or Create an Application Load Balancer (ALB)
1. Open the **AWS Management Console** and navigate to **EC2** -> **Load Balancers** (under Load Balancing in the left sidebar).
2. If you already have an Application Load Balancer, select it. If not, click **Create load balancer**, select **Application Load Balancer**, and create a basic one (it doesn't need registered targets for this audit simulation).
3. Find your ALB's **ARN** in the details tab. 
4. Extract the **Load Balancer Suffix** from the ARN.
   - For example, if your ARN is: `arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188`
   - The suffix is: `app/my-load-balancer/50dc6c495c0c9188`
   *Keep this suffix handy for Step 4.*

<details open>
<summary>📸 Step 1 Screenshots (ALB Setup & Configuration)</summary>

| | |
|:---:|:---:|
| ![ALB Creation 1](./images/ALB_Creation1.png) | ![ALB Creation 2](./images/ALB_Creation2.png) |
| ![ALB Creation 3](./images/ALB_Creation3.png) | ![ALB Creation 4](./images/ALB_Creation4.png) |
| ![ALB Creation 5](./images/ALB_Creation5.png) | ![ALB Creation 6](./images/ALB_Creation6.png) |
| ![ALB Creation 7](./images/ALB_Creation7.png) | |

</details>

---

### Step 2: Create or Reuse the SNS Topic
1. Navigate to the **SNS Console**.
2. Create a new standard topic (e.g., `ELB5xxAlertTopic`) or reuse your existing subscription topic.
3. Ensure your email is subscribed to the topic and the status is **Confirmed**.

<details open>
<summary>📸 Step 2 Screenshots (SNS Topic & Subscription)</summary>

| | |
|:---:|:---:|
| ![SNS Topic 1](./images/SNS_Topic1.png) | ![SNS Topic 2](./images/SNS_Topic2.png) |
| ![SNS Subscription 1](./images/SNS_Subscription1.png) | ![SNS Subscription 2](./images/SNS_Subscription2.png) |
| ![SNS Subscription 3](./images/SNS_Subscription3.png) | ![SNS Subscription 4](./images/SNS_Subscription4.png) |
| ![Email Validation](./images/Email_Validation.png) | |

</details>

---

### Step 3: Create the IAM Role for Lambda
1. Navigate to the **IAM Console** -> **Roles** -> **Create role**.
2. Choose **AWS service** -> **Lambda as the trusted use case. Click Next.**
3. Create a custom policy (or attach `CloudWatchReadOnlyAccess` and `AmazonSNSFullAccess`) to grant these permissions:
   - `cloudwatch:GetMetricStatistics`
   - `sns:Publish`
   - CloudWatch Logs write permissions (`logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`).
4. Name the role `LambdaCloudWatchSNSRole` and click **Create role**.

<details open>
<summary>📸 Step 3 Screenshots (IAM Policy & Role Setup)</summary>

| | |
|:---:|:---:|
| ![IAM Policy 1](./images/IAM_Policy1.png) | ![IAM Policy 2](./images/IAM_Policy2.png) |
| ![IAM Policy 3](./images/IAM_Policy3.png) | ![IAM Role 1](./images/IAM_Role1.png) |
| ![IAM Role 2](./images/IAM_Role2.png) | ![IAM Role 3](./images/IAM_Role3.png) |
| ![IAM Role 4](./images/IAM_Role4.png) | |

</details>

---

### Step 4: Create the AWS Lambda Function
1. Navigate to the **Lambda Console** and click **Create function**.
2. Configure settings:
   - **Function name**: `ELB5xxMonitor`
   - **Runtime**: `Python 3.x` (e.g., Python 3.13)
   - **Execution role**: Choose **Use an existing role** and select `LambdaCloudWatchSNSRole`.
3. Click **Create function**.
4. Paste the code from [lambda_function.py](./lambda_function.py) into the editor and click **Deploy**.
5. Go to **Configuration** tab -> **Environment variables** -> **Edit** and add:
   - **Key**: `SNS_TOPIC_ARN`, **Value**: `<your-sns-topic-arn>`
   - **Key**: `LOAD_BALANCER_SUFFIX`, **Value**: `<your-extracted-alb-suffix>`
   - **Key**: `THRESHOLD`, **Value**: `5` (or your preferred value)
6. Click **Save**.

<details open>
<summary>📸 Step 4, 5 & 6 Screenshots (Lambda Function, Trigger & Testing)</summary>

| | |
|:---:|:---:|
| ![Lambda 1](./images/Lambda1.png) | ![Lambda 2](./images/Lambda2.png) |
| ![Lambda 3](./images/Lambda3.png) | ![Lambda 4](./images/Lambda4.png) |
| ![Lambda 5](./images/Lambda5.png) | ![Lambda 6](./images/Lambda6.png) |

</details>

---

### Step 5: Configure the CloudWatch/EventBridge Scheduled Trigger
1. In the Lambda **Function overview** block, click **Add trigger**.
2. Select **EventBridge (CloudWatch Events)** from the dropdown.
3. Choose **Create a new rule**.
   - **Rule name**: `ELB5xxCheckSchedule`
   - **Rule type**: `Schedule expression`
   - **Schedule expression**: `rate(5 minutes)` (triggers the Lambda every 5 minutes)
4. Click **Add**.

---

### Step 6: Test and Simulate 5xx Errors Spike
Since you won't easily have 5 real 5xx errors on your test load balancer, you can simulate a spike to verify that your email alerts are working:

1. **Option A: Lower the Threshold**
   - Go to your Lambda's **Environment variables** and change the `THRESHOLD` value to `-1`.
   - Run a manual test with an empty JSON test payload (`{}`). 
   - Even if the metric reports `0.0` errors, it will exceed the `-1` threshold and trigger the email alert.

2. **Option B: Modify Code Fallback (Fallback Simulation)**
   - In [lambda_function.py](./lambda_function.py), temporarily modify **line 49** where it handles empty data points:
     - Change `error_sum = 0.0` to `error_sum = 15.0`.
   - Deploy the changes and click **Test**.
   - This will force the script to simulate 15 errors and send the email notification.
   - Once tested, revert the line back to `error_sum = 0.0` and deploy.

---

## Example Screenshots Gallery

All step-by-step screenshots are embedded inline within each corresponding configuration step above. Open the `<details open>` dropdown panels to view:
* **Step 1:** Application Load Balancer (ALB) creation and details.
* **Step 2:** SNS Topic creation, email subscription, and validation setup.
* **Step 3:** IAM Policy and Lambda execution role configuration.
* **Step 4, 5 & 6:** Lambda setup, environment variables, EventBridge rule triggers, log executions, and email alert delivery.
