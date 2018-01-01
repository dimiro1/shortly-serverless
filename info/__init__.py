"""Responsible to handle get info urls"""

import sys
import os
import json
import boto3

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "../"))
sys.path.append(os.path.join(HERE, "../lib"))

from services import shortly, mocks, hasher, aws

DYNAMODB = boto3.resource('dynamodb')

SHORTLY = shortly.Shortly(
    hasher.Hasher(), aws.AtomicCounter(), aws.Database(DYNAMODB), mocks.Notifier())


def handler(event, context):
    """Return information data of the url"""
    try:
        info = SHORTLY.info(event['pathParameters']['id'])
        return respond(200, {
            'id': info['Item']['id'],
            'long_url': info['Item']['long_url']
        })
    except shortly.InternalError:
        return respond(500, {'message': 'Internal server error'})
    except shortly.NotFound:
        return respond(404, {'message': 'Not found'})


def respond(code, data):
    """helper function to respond json with the given status code and the given data"""
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data)
    }
