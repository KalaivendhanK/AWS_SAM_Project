import json

import boto3
import base64
from botocore.exceptions import ClientError

# Creating a boto session with profile as local stack. This is not necessary to set up but is good practice

local_stack = boto3.session.Session(profile_name='localstack')

# Creating the low level functional client
client = local_stack.client(
    's3',
    aws_access_key_id='localstackaccesskey',
    aws_secret_access_key='localstacksecretkey',
    region_name='us-east-1',
    endpoint_url='http://localhost:4566'
)

# Creating the high level object oriented interface
resource = local_stack.resource(
    's3',
    aws_access_key_id='localstackaccesskey',
    aws_secret_access_key='localstacksecretkey',
    region_name='us-east-1',
    endpoint_url='http://localhost:4566'
)

# Fetch the list of existing buckets
clientResponse = client.list_buckets()

# Print the bucket names one by one
print('Printing bucket names...')
for bucket in clientResponse['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')

# Create the bucket
new_bucket_name='sql-server-shack-demo-3'
location = {'LocationConstraint': 'ap-south-1'}
try:
    client.create_bucket(
        Bucket=new_bucket_name,
        CreateBucketConfiguration=location
    )
    print(f"Bucket created: {new_bucket_name}")
except Exception as e:
    print(e)


def get_secret():
    session = boto3.session.Session(profile_name="localstack")
    secret_manager_client = session.client(
        endpoint_url="https://localhost:4566",
        service_name='secretsmanager',
        region_name='us-east-1',
        verify=False
    )

    try:
        get_secret_value_response = secret_manager_client.get_secret_value(
            SecretId="redshift/rotation"
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            # print(secret)
            creds = json.loads(secret)
            return creds
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            print(decoded_binary_secret)


print(get_secret())
