# Some set-up on S3

1. Create a bucket
    ```bash
    awslocal s3 mb s3://blog-bucket
   # check the bucket
    awslocal s3 ls
    ```
2. Create a policy
    ```bash
    awslocal s3api put-bucket-policy --bucket blog-bucket --policy '{
    "Version": "2012-10-17",
    "Statement": [
    {
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::blog-bucket/*"
    }
    ]
    }'
    ```
    ```bash
    awslocal s3api put-bucket-cors --bucket e-commerce --cors-configuration '{
    "CORSRules": [
        {
            "AllowedOrigins": ["*"],
            "AllowedMethods": ["GET"],
            "AllowedHeaders": ["*"]
        }
    ]
    }'
    ```
3. Setup on the `settings.py`

```python
AWS_ACCESS_KEY_ID = 'test '
AWS_SECRET_ACCESS_KEY = 'test'
AWS_STORAGE_BUCKET_NAME = 'blog-bucket'
AWS_S3_SIGNATURE_NAME = '',
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = False
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = "http://localhost:4566"
```
