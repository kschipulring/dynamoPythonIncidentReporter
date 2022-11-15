import boto3
import install_table

#gets the core table for the app for use in calls by the other python fi
def getMainTable():
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
	
	table_name = 'incident_reports'
    
	try:
		table = dynamodb.Table(table_name)
	except:
		#install if not already existing
		table = install_table.install(table_name)
    
    return table
