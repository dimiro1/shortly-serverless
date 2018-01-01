"""Responsible to expand urls"""

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
    """Expand url handler"""
    try:
        info = SHORTLY.info(event['pathParameters']['id'])
        # Trigger event to increment stats
        return redirect(info['Item']['long_url'])
    except shortly.InternalError:
        return respond(500, {'message': 'Internal server error'})
    except shortly.NotFound:
        return respond(404, {'message': 'Not found'})


def respond(code, data):
    """Helper function to respond json with the given status code and the given data"""
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data)
    }


def redirect(url):
    """Helper function to make an http redirect to the given URL"""
    return {
        'statusCode': 301,
        'headers': {
            'Location': url
        },
        'body': json.dumps({'url': url})
    }
