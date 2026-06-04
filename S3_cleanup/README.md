# Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

## Objective
Automatically delete files older than 30 days in a specific Amazon S3 bucket using an AWS Lambda function triggered manually or periodically.

---

## Step-by-Step Instructions

### Step 1: Set Up the S3 Bucket
1. Open the **AWS Management Console** and navigate to the **S3** service.
2. Click **Create bucket**.
3. Enter a unique bucket name (e.g., `my-automated-cleanup-bucket-<your-name>`) and choose your preferred AWS Region.
4. Keep the default settings (Block public access enabled, default encryption enabled) and click **Create bucket**.
5. Upload a few test files (e.g., `file1.txt`, `file2.txt`, `image.jpg`).
   > *Note: S3 objects have a read-only `LastModified` date set on creation. To simulate files older than 30 days without waiting, you will temporarily adjust the retention threshold in the Lambda function to `0` days during testing so that all current files are cleaned up.*

---

### Step 2: Create the IAM Role for Lambda
1. Navigate to the **IAM Console**.
2. Select **Roles** from the left navigation pane and click **Create role**.
3. Choose **AWS service** as the trusted entity type, and select **Lambda** under service use cases. Click **Next**.
4. Search for and attach the policy **`AmazonS3FullAccess`** (in production, you would restrict this to your specific bucket, but this is fine for this assignment). Click **Next**.
5. Name the role `LambdaS3CleanupRole` and click **Create role**.

---

### Step 3: Set Up the AWS Lambda Function
1. Navigate to the **Lambda Console** and click **Create function**.
2. Select **Author from scratch**.
3. Configure the settings:
   - **Function name**: `S3BucketCleanup`
   - **Runtime**: `Python 3.x` (e.g., Python 3.12)
   - **Execution role**: Choose **Use an existing role** and select `LambdaS3CleanupRole` from the list.
4. Click **Create function**.
5. In the Lambda Editor:
   - Double-click `lambda_function.py`.
   - Replace the default code with the code provided in [lambda_function.py](./lambda_function.py).
   - Click **Deploy** to save and compile the changes.

---

### Step 4: Configure Environment Variables
1. In the Lambda function console, click on the **Configuration** tab.
2. Select **Environment variables** from the sidebar and click **Edit**.
3. Add a new variable:
   - **Key**: `BUCKET_NAME`
   - **Value**: Name of the S3 bucket you created in Step 1.
4. Click **Save**.

---

### Step 5: Test and Verify the Cleanup
1. Click on the **Test** tab in your Lambda console.
2. Create a new test event:
   - **Event name**: `TestCleanup`
   - **Event JSON**: `{}` (leave empty JSON object)
3. Click **Save**.

#### 🧪 Testing "Older than 30 days" Simulation:
1. To test the cleanup immediately on your newly uploaded files, modify **line 19** in your Lambda function code:
   - Change `retention_days = 30` to `retention_days = 0` (this targets all files for immediate cleanup).
2. Click **Deploy**.
3. Click **Test**.
4. Review the **Execution Results**:
   - The status should show **Succeeded**.
   - The log output will list all the deleted test files.
5. Navigate back to your S3 bucket. Refresh the page to verify that the files have been successfully deleted.
6. Change the code back to `retention_days = 30` and deploy it again to finalize the deployment.

---

## Required Screenshots for Submission

Make sure to capture and save the following screenshots in this directory (e.g., in an `images/` subfolder):

1. **`01_s3_bucket_files.png`**: The S3 bucket overview showing your uploaded test files *before* running the cleanup.
2. **`02_lambda_env_variables.png`**: The Lambda "Configuration -> Environment variables" tab showing `BUCKET_NAME`.
3. **`03_lambda_test_execution.png`**: The Lambda **Execution Results** console output showing status `Succeeded` and list of deleted files.
4. **`04_s3_bucket_after_cleanup.png`**: The S3 bucket overview showing that the older/all test files have been deleted.
5. **`05_cloudwatch_logs.png`**: The CloudWatch Logs stream for this Lambda run showing the detailed print statements.
