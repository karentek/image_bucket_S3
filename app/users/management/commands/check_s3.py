import os
from django.core.management.base import BaseCommand
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


class Command(BaseCommand):
    help = 'Check S3 connection and upload a test file'

    def handle(self, *args, **kwargs):
        s3_client = boto3.client('s3',
                                 region_name=os.getenv('AWS_DEFAULT_REGION'),
                                 endpoint_url=os.getenv('STORAGE_ENDPOINT'),
                                 aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                 aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

        bucket_name = os.getenv('BUCKET_NAME')
        test_file_key = 'test_file.txt'
        test_file_content = b'This is a test file for checking S3 connection.'
        try:
            # Upload a test file
            s3_client.put_object(Bucket=bucket_name, Key=test_file_key, Body=test_file_content)
            self.stdout.write(self.style.SUCCESS(f'Successfully uploaded {test_file_key} to {bucket_name}'))

            # Retrieve the test file
            response = s3_client.get_object(Bucket=bucket_name, Key=test_file_key)
            retrieved_content = response['Body'].read()

            if retrieved_content == test_file_content:
                self.stdout.write(self.style.SUCCESS(f'Successfully retrieved {test_file_key} from {bucket_name}'))
            else:
                self.stdout.write(self.style.ERROR(f'Content mismatch for {test_file_key}'))

        except NoCredentialsError:
            self.stdout.write(self.style.ERROR('Credentials not available'))
        except ClientError as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))