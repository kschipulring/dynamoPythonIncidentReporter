import db_core
import boto3
from boto3.dynamodb.conditions import Key, Attr

#just one person. Optional second parameter for when you only want certain attributes
def get(id, attribs=[]):
    table = db_core.getMainTable()
    
    #if we just want certain attributes returned from DynamoDB
    if len(attribs) > 0:
        r = table.get_item(Key={'person_id': id, 'record_type': 'person'}, AttributesToGet=attribs)
    else:
        r = table.get_item(Key={'person_id': id, 'record_type': 'person'})
    
    return r
