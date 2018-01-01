"""Responsible to handle Create short urls"""

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
    """Create short url handler"""
    if event['body'] is None:
        return respond(400, {'message': 'Bad request'})

    body = json.loads(event['body'])

    if body['long_url'] is None:
        return respond(400, {'message': 'Bad request'})

    try:
        info = SHORTLY.create(body['long_url'])
        return respond(200, info)
    except shortly.InternalError:
        return respond(500, {'message': 'Internal server error'})


def respond(code, data):
    """helper function to respond json with the given status code and the given data"""
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data)
    }
