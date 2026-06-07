# Monitor EC2 Instance State Changes Using AWS Lambda, Boto3, and SNS

## Objective
Automatically monitor EC2 instance state transitions (such as starting, stopping, or terminating) using Amazon EventBridge, parse the state changes in AWS Lambda, and dispatch email alerts via Amazon SNS.

---

## Step-by-Step Instructions

### Step 1: Set Up an EC2 Instance
1. Open the **AWS Management Console** and navigate to **EC2**.
2. If you do not have any running or stopped instances, launch a new free-tier instance (e.g., `t2.micro` running Amazon Linux).
3. Keep it running or stopped. Note down the **Instance ID** (e.g., `i-0abcdef123456789f`).

<details>
<summary>📸 Click to view EC2 Instance Setup Screenshots</summary>

| Launching Instance | Configuring Instance |
|:---:|:---:|
| ![EC2 Creation 1](./images/EC2_Creation1.png) | ![EC2 Creation 2](./images/EC2_Creation2.png) |
| ![EC2 Creation 3](./images/EC2_Creation3.png) | ![EC2 Creation 4](./images/EC2_Creation4.png) |
| ![EC2 Creation 5](./images/EC2_Creation5.png) | ![EC2 Creation 6](./images/EC2_Creation6.png) |

</details>

---

### Step 2: Create or Reuse the SNS Topic
1. Navigate to the **SNS Console**.
2. Select **Topics** -> Create a standard topic (e.g., `EC2StateAlertTopic`) or reuse an existing one.
3. Ensure your email is subscribed and status is **Confirmed**.

<details>
<summary>📸 Click to view SNS Topic & Subscription Setup Screenshots</summary>

| SNS Topic Setup | SNS Subscription Setup |
|:---:|:---:|
| ![SNS Topic 1](./images/SNS_Topic1.png) | ![SNS Subscription 1](./images/SNS_Subscription1.png) |
| ![SNS Topic 2](./images/SNS_Topic2.png) | ![SNS Subscription 2](./images/SNS_Subscription2.png) |
| ![SNS Subscription 3](./images/SNS_Subscription3.png) | ![SNS Subscription 4](./images/SNS_Subscription4.png) |
| ![SNS Subscription 5](./images/SNS_Subscription5.png) | ![SNS Subscription 6](./images/SNS_Subscription6.png) |

</details>

---

### Step 3: Create the IAM Role for Lambda
1. Navigate to the **IAM Console** -> **Roles** -> **Create role**.
2. Select **AWS service** -> **Lambda** as the trusted use case. Click **Next**.
3. Create or attach a policy granting:
   - `sns:Publish`
   - CloudWatch Logs write access (`logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`).
4. Name the role `LambdaEC2SNSRole` and click **Create role**.

<details>
<summary>📸 Click to view IAM Role Configuration Screenshots</summary>

| Policy Definition | Role Creation |
|:---:|:---:|
| ![IAM Policy 1](./images/IAM_Policy1.png) | ![IAM Policy 2](./images/IAM_Policy2.png) |
| ![IAM Policy 3](./images/IAM_Policy3.png) | ![IAM Policy 4](./images/IAM_Policy4.png) |
| ![IAM Policy 5](./images/IAM_Policy5.png) | ![IAM Policy 6](./images/IAM_Policy6.png) |
| ![IAM Policy 7](./images/IAM_Policy7.png) | |

</details>

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

<details>
<summary>📸 Click to view Lambda Function Configuration Screenshots</summary>

| Lambda Function Setup | Environment Variables |
|:---:|:---:|
| ![Lambda 1](./images/Lambda1.png) | ![Lambda 2](./images/Lambda2.png) |
| ![Lambda 3](./images/Lambda3.png) | ![Lambda 4](./images/Lambda4.png) |
| ![Lambda 5](./images/Lambda5.png) | |

</details>

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

<details>
<summary>📸 Click to view EventBridge Rule Setup Screenshots</summary>

| EventBridge Rule Creation | Targets & Settings |
|:---:|:---:|
| ![EventBridge 1](./images/EventBridge1.png) | ![EventBridge 2](./images/EventBridge2.png) |
| ![EventBridge 3](./images/EventBridge3.png) | ![EventBridge 4](./images/EventBridge4.png) |
| ![EventBridge 5](./images/EventBridge5.png) | ![EventBridge 6](./images/EventBridge6.png) |
| ![EventBridge 7](./images/EventBridge7.png) | ![EventBridge 8](./images/EventBridge8.png) |
| ![EventBridge 9](./images/EventBridge9.png) | |

</details>

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

<details>
<summary>📸 Click to view Testing & State Verification Screenshots</summary>

| Testing & Transition | Verification & Logs |
|:---:|:---:|
| ![EC2 State Change 1](./images/EC2StateChange1.png) | ![EC2 State Change 2](./images/EC2StateChange2.png) |
| ![EC2 State Change 3](./images/EC2StateChange3.png) | ![EC2 State Change 4](./images/EC2StateChange4.png) |
| ![EC2 State Change 5](./images/EC2StateChange5.png) | ![EC2 State Change 6](./images/EC2StateChange6.png) |

</details>

---

## Example Screenshots Gallery

All screenshots are categorized and embedded inline within each corresponding setup step above. You can open the dropdown menu in each step to view:
* **Step 1:** EC2 instance creation and configuration details.
* **Step 2:** SNS Topic and Email Subscription setup.
* **Step 3:** IAM policy and Lambda execution role configuration.
* **Step 4:** Lambda function deployment and Environment Variables configuration.
* **Step 5:** EventBridge rule creation, event patterns, and Lambda function target mapping.
* **Step 6:** EC2 instance state-change trigger execution, received email alerts, and CloudWatch logs verification.
