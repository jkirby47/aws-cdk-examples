# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import os
import json
import logging
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")


def handler(event, context):
    table = os.environ.get("TABLE_NAME")
    
    # Log security-relevant context
    request_context = event.get("requestContext", {})
    logger.info(f"Request ID: {context.request_id}")
    logger.info(f"Source IP: {request_context.get('identity', {}).get('sourceIp', 'unknown')}")
    logger.info(f"User Agent: {request_context.get('identity', {}).get('userAgent', 'unknown')}")
    logger.info(f"Request Time: {request_context.get('requestTime', 'unknown')}")
    logger.info(f"Table: {table}")
    
    if event["body"]:
        item = json.loads(event["body"])
        logger.info(f"Payload received: {item}")
        year = str(item["year"])
        title = str(item["title"])
        id = str(item["id"])
        dynamodb_client.put_item(
            TableName=table,
            Item={"year": {"N": year}, "title": {"S": title}, "id": {"S": id}},
        )
        message = "Successfully inserted data!"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
    else:
        logger.info("Received request without payload")
        dynamodb_client.put_item(
            TableName=table,
            Item={
                "year": {"N": "2012"},
                "title": {"S": "The Amazing Spider-Man 2"},
                "id": {"S": str(uuid.uuid4())},
            },
        )
        message = "Successfully inserted data!"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
