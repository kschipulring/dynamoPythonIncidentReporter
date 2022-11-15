import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import STRING

#can use a different table name if desired
def install(table_name="incident_reports"):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    table = dynamodb.create_table(
        TableName=table_name,
		KeySchema=[
			{'AttributeName': 'person_id', 'KeyType': 'HASH'},  # Partition key
			{'AttributeName': 'record_type', 'KeyType': 'RANGE'}  # Sort key
		],
		AttributeDefinitions=[
			{'AttributeName': 'person_id', 'AttributeType': STRING},
			{'AttributeName': 'record_type', 'AttributeType': STRING}
		],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )
	
	#make sure it finishes being set up before returning. NOTE: should not be too long with this one.
	table.wait_until_exists()
	
	
	## Now add a Global Secondary Index so that we can choose only people or only institutions, roles, etc. if we wanted to.
	
	# Attrs for GSI
	attrdef = [
		{"AttributeName": "record_type", "AttributeType": STRING}
	]
	
	# Asset ID index definition
	recordTypeIdx = [
		{"Create": {
				"IndexName": "record_type-index",
				"KeySchema": [{
					"AttributeName": "record_type",
					"KeyType": "HASH"
				}],
				'Projection': {
					'ProjectionType': "ALL",
				},
				'ProvisionedThroughput': {
					'ReadCapacityUnits': 5,
					'WriteCapacityUnits': 5
				}
			}
		},
	]
	
	# now add the GSI to the table
	table.update(AttributeDefinitions=attrdef, GlobalSecondaryIndexUpdates=recordTypeIdx)
	
	return table
