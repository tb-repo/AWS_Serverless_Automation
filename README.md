# AWS Serverless Automation Assignments

This repository contains few useful basic AWS automation solutions implemented using **AWS Lambda**, **Boto3**, **DynamoDB**, **SNS**, **CloudWatch/EventBridge**, and **Amazon S3**.

Each project is self-contained with its own Python Lambda code and dedicated documentation (including step-by-step setup guides and screenshot requirements).

---

## Project Structure

| Solution | Service Focus | Directory |
|---|---|---|
| **S3 Bucket Cleanup Automation** | S3 Bucket | [S3 Cleanup](./S3_cleanup/) |
| **S3 Encryption Status Automation** | S3 Security | [S3 Encryption Monitor](./S3_encryption_monitor/) |
| **DynamoDB SNS Alert Automation** | DynamoDB & SNS | [DynamoDB SNS Alert](./DynamoDB_SNS_alert/) |
| **ELB 5xx Alert Automation** | ELB & CloudWatch | [ELB 5xx Alert](./ELB_5xx_alert/) |
| **EC2 State Monitor Automation** | EC2 & EventBridge | [EC2 State Monitor](./EC2_state_monitor/) |

---

## General Prerequisites
To run these automations successfully, make sure you have:
1. An active **AWS Account** with sufficient permissions to manage EC2, S3, DynamoDB, SNS, CloudWatch, and IAM.
2. The **AWS CLI** configured on your local machine (optional, if you want to run tests locally).
3. **Python 3.x** installed.
