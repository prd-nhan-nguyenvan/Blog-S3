import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from django.core.management.base import BaseCommand

from blogapp.models import Blog


class Command(BaseCommand):
    help = (
        'Migrate files from one S3 bucket to another and update the database.')

    def handle(self, *args, **kwargs):
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        # Source and destination bucket names
        source_bucket = 'blog-bucket'
        destination_bucket = 'new-blog-bucket'

        try:
            response = s3.list_objects_v2(Bucket=source_bucket)
            if 'Contents' not in response:
                self.stdout.write(self.style.SUCCESS('No files to migrate.'))
                return

            for obj in response['Contents']:
                # Copy each file from source to destination
                source_key = obj['Key']
                destination_key = source_key  # Keep the same key in the new
                # bucket
                copy_source = {'Bucket': source_bucket, 'Key': source_key}

                # Perform the copy operation
                s3.copy_object(CopySource=copy_source,
                               Bucket=destination_bucket, Key=destination_key)

                # After copying, update the corresponding blog entry in the
                # database
                blog = Blog.objects.filter(
                    main_image=f's3://{source_bucket}/{source_key}').first()
                if blog:
                    # Update the image URL in the database to point to the
                    # new bucket
                    new_url = (f'http://localhost:4566/{destination_bucket}/'
                               f'{destination_key}')
                    blog.main_image = new_url  # Assuming `main_image` is a
                    # URL field
                    blog.save()

                self.stdout.write(self.style.SUCCESS(
                    f'Migrated {source_key} to {destination_bucket}.'))

        except NoCredentialsError:
            self.stdout.write(
                self.style.ERROR('Credentials not found for LocalStack.'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error migrating files: {str(e)}'))
