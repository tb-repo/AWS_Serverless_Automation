# AWS Serverless Automation Assignments

This repository contains five AWS serverless automation solutions implemented using **AWS Lambda**, **Boto3**, **DynamoDB**, **SNS**, **CloudWatch/EventBridge**, and **Amazon S3**.

Each project is self-contained with its own Python Lambda code and dedicated documentation (including step-by-step setup guides and screenshot requirements).

---

## 📂 Project Structure

| Assignment | Service Focus | Directory | Status |
|---|---|---|---|
| **Assignment 2** | S3 Bucket | [S3 Cleanup](./S3_cleanup/) | 📝 In Progress |
| **Assignment 3** | S3 Security | [S3 Encryption Monitor](./S3_encryption_monitor/) | 📝 In Progress |

| **Assignment 7** | DynamoDB & SNS | [DynamoDB SNS Alert](./DynamoDB_SNS_alert/) | 📝 In Progress |

| **Assignment 10** | ELB & CloudWatch | [ELB 5xx Alert](./ELB_5xx_alert/) | 📝 In Progress |

| **Assignment 14** | EC2 & EventBridge | [EC2 State Monitor](./EC2_state_monitor/) | 📝 In Progress |


---

## 🚀 How to Synchronize with GitHub

To push your changes to your remote GitHub repository, run the following commands from your terminal in this directory:

```bash
# Check git status
git status

# Add all files (lambda scripts, READMEs, screenshots)
git add .

# Commit changes
git commit -m "Add S3 cleanup implementation files and documentation templates"

# Push to main branch
git push origin main
```

---

## 🛠️ General Prerequisites
To run these assignments successfully, make sure you have:
1. An active **AWS Account** with sufficient permissions to manage EC2, S3, DynamoDB, SNS, CloudWatch, and IAM.
2. The **AWS CLI** configured on your local machine (optional, if you want to run tests locally).
3. **Python 3.x** installed.
