import json
import os
import boto3
import botocore
import uuid

def handler(event, context):
    lambda_client = boto3.client("lambda")
    lambda_client.invoke(
        FunctionName="lambda-chat-dock",
        InvocationType="Event",
        Payload= json.dumps(event)
    )
    return {
            'statusCode': 200,
            'body': json.dumps({"lambda": "invoked"})
        }