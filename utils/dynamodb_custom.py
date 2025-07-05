import os
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

users_table = dynamodb.Table('users')
carts_table = dynamodb.Table('carts')
orders_table = dynamodb.Table('orders')

def get_user(username):
    try:
        response = users_table.get_item(Key={'username': username})
        return response.get('Item')
    except ClientError:
        return None

def add_user(username, email, password_hash):
    try:
        users_table.put_item(Item={
            'username': username,
            'email': email,
            'password': password_hash
        }, ConditionExpression='attribute_not_exists(username)')
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return False
        raise

def get_cart(username):
    response = carts_table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    return response.get('Items', [])

def add_to_cart(username, name, price, image):
    try:
        carts_table.update_item(
            Key={'username': username, 'name': name},
            UpdateExpression='SET qty = if_not_exists(qty, :zero) + :inc, price=:price, image=:image',
            ExpressionAttributeValues={':inc': 1, ':zero': 0, ':price': price, ':image': image},
            ReturnValues='UPDATED_NEW'
        )
    except ClientError as e:
        raise

def remove_from_cart(username, name):
    carts_table.delete_item(Key={'username': username, 'name': name})

def clear_cart(username):
    items = get_cart(username)
    for item in items:
        carts_table.delete_item(Key={'username': username, 'name': item['name']})

def get_orders(username):
    response = orders_table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    return response.get('Items', [])

def add_order(username, name, price, image, qty):
    orders_table.put_item(Item={
        'username': username,
        'name': name,
        'price': price,
        'image': image,
        'qty': qty
    })
