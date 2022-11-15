import json
import boto3

import chalice

import person

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    table = dynamodb.Table('incident_reports')
    
    r = table.get_item(Key={'person_id': 'abc123', 'record_type': 'institution'})
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps( person.get("abc123") )
    }
