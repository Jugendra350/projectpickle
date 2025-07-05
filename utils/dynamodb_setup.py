import boto3
import os

def create_tables():
    # Use environment variables for AWS credentials and region
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_REGION', 'us-east-1')

    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )

    # User Table
    try:
        user_table = dynamodb.create_table(
            TableName='Users',
            KeySchema=[
                {'AttributeName': 'email', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print('Creating Users table...')
        user_table.wait_until_exists()
        print('Users table created.')
    except Exception as e:
        print(f'Users table: {e}')

    # Product Table
    try:
        product_table = dynamodb.create_table(
            TableName='Products',
            KeySchema=[
                {'AttributeName': 'product_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'product_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print('Creating Products table...')
        product_table.wait_until_exists()
        print('Products table created.')
    except Exception as e:
        print(f'Products table: {e}')

    # Orders Table
    try:
        order_table = dynamodb.create_table(
            TableName='Orders',
            KeySchema=[
                {'AttributeName': 'order_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'order_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print('Creating Orders table...')
        order_table.wait_until_exists()
        print('Orders table created.')
    except Exception as e:
        print(f'Orders table: {e}')

if __name__ == '__main__':
    create_tables()
