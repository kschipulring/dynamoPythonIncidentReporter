import boto3

#gets the core table for the app for use in calls by the other python fi
def getMainTable():
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    table = dynamodb.Table('incident_reports')
    
    return table
