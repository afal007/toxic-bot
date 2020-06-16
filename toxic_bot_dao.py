import time
import boto3

from boto3.dynamodb.conditions import Key

ATTRIBUTE_CHAT_ID = 'ChatId'
ATTRIBUTE_USED_BET = 'UsedBet'
ATTRIBUTE_DATA_TYPE = 'DataType'
ATTRIBUTE_LAST_NAME = 'LastName'
ATTRIBUTE_USER_NAME = 'TelegramUsername'
ATTRIBUTE_FIRST_NAME = 'FirstName'
ATTRIBUTE_BET_USER_NAME = 'BetUserName'

BET = 'BET'
DATA = 'DATA'

dynamodb = boto3.resource('dynamodb')


def put_data(chat_id, user):
    user_table = dynamodb.Table('User')
    user_table.put_item(
        Item={
            ATTRIBUTE_CHAT_ID: str(chat_id),
            ATTRIBUTE_DATA_TYPE: DATA,
            ATTRIBUTE_USER_NAME: user.username
        }
    )


def put_bet(chat_id, bet_username):
    user_table = dynamodb.Table('User')
    user_table.put_item(
        Item={
            ATTRIBUTE_CHAT_ID: str(chat_id),
            ATTRIBUTE_DATA_TYPE: BET + '-' + str(chat_id) + '-' + str(time.time_ns()),
            ATTRIBUTE_BET_USER_NAME: bet_username
        }
    )


def get_data(chat_id):
    user_table = dynamodb.Table('User')
    return user_table.get_item(Key={ATTRIBUTE_CHAT_ID: str(chat_id), ATTRIBUTE_DATA_TYPE: DATA})['Item']


def set_used_bet(chat_id):
    user_table = dynamodb.Table('User')
    user_table.update_item(
        Key={
            ATTRIBUTE_CHAT_ID: str(chat_id),
            ATTRIBUTE_DATA_TYPE: DATA
        },
        UpdateExpression="set " + ATTRIBUTE_USED_BET + " = :val",
        ExpressionAttributeValues={
            ':val': True
        }
    )


def has_bets(chat_id):
    user_table = dynamodb.Table('User')
    response = user_table.scan(
        FilterExpression=Key(ATTRIBUTE_CHAT_ID).eq(str(chat_id)) & Key(ATTRIBUTE_DATA_TYPE).begins_with(BET)
    )
    return len(response['Items']) > 0
