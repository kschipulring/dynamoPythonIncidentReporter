import boto3

def get(id):
        
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    table = dynamodb.Table('incident_reports')
    
    r = table.get_item(Key={'person_id': id, 'record_type': 'person'}, AttributesToGet=['last_name'])
    
    return r
