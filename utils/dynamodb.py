import os
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

users_table = dynamodb.Table('Users')
carts_table = dynamodb.Table('Carts')
orders_table = dynamodb.Table('Orders')

# User functions
def get_user(email):
    try:
        response = users_table.get_item(Key={'email': email})
        return response.get('Item')
    except ClientError:
        return None

def add_user(email, password_hash):
    try:
        users_table.put_item(Item={
            'email': email,
            'password': password_hash
        }, ConditionExpression='attribute_not_exists(email)')
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return False
        raise

# Cart functions
def get_cart(email):
    response = carts_table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    return response.get('Items', [])

def add_to_cart(email, name, price, image):
    try:
        carts_table.update_item(
            Key={'email': email, 'name': name},
            UpdateExpression='SET qty = if_not_exists(qty, :zero) + :inc, price=:price, image=:image',
            ExpressionAttributeValues={':inc': 1, ':zero': 0, ':price': price, ':image': image},
            ReturnValues='UPDATED_NEW'
        )
    except ClientError as e:
        raise

def remove_from_cart(email, name):
    carts_table.delete_item(Key={'email': email, 'name': name})

def clear_cart(email):
    items = get_cart(email)
    for item in items:
        carts_table.delete_item(Key={'email': email, 'name': item['name']})

# Order functions
def get_orders(email):
    response = orders_table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    return response.get('Items', [])

def add_order(email, name, price, image, qty):
    orders_table.put_item(Item={
        'email': email,
        'name': name,
        'price': price,
        'image': image,
        'qty': qty
    })
