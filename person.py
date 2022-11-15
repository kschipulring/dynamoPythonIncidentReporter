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

    
#multiple people QUERY 
def getQuery(attribs=[]):
    table = db_core.getMainTable()
    
    r = ""
    
    #if we just want certain attributes returned from the DynamoDB table
    if len(attribs) > 0:

        #similar to Javascript string join
        projection_expression = ', '.join(attribs)
        
        r = table.query(
            IndexName='record_type-index',
            KeyConditionExpression=Key('record_type').eq('person'),
            Select= 'SPECIFIC_ATTRIBUTES',
            ProjectionExpression= projection_expression
        )
    else:

        #all attributes, no matter what
        r = table.query(
			IndexName='record_type-index',
			KeyConditionExpression= Key('record_type').eq('person')
		)

    #KeyConditionExpression=Key('person_id').eq('abc123') & Key('record_type').eq('institution')
    
    return r

