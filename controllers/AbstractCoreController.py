from abc import ABC, abstractmethod

import boto3
from boto3.dynamodb.conditions import Key, Attr

#import sys
#sys.path.append('../ddb')
import ddb.db_core as db_core

class AbstractCoreController(ABC):

    def __init__(self):
        self.table = db_core.getMainTable()
        super().__init__()

    #just one person. Optional second parameter for when you only want certain attributes
    @abstractmethod
    def get(self, id, record_type, attribs_returned=[]):
        pass

    #get a certain kind of a record associated with a person's id
    def getRecordByPersonId(self, record_type, attribs_returned=[]):
        r = ""

        """
        in spite of the possibility that the record type may be something other
        than a person, 'person_id' is still a primary key
        """
        kwargs = {"Key": {'person_id': id, 'record_type': record_type}}
        
        #if we just want certain attributes returned from DynamoDB
        if len(attribs_returned) > 0:
            kwargs["AttributesToGet"] = attribs_returned

        r = self.table.get_item(**kwargs)

        return r


    #multiple record QUERY of a particular record_type
    def getQuery(self, record_type, key_condition_kwargs=None, attribs=[]):
        table = db_core.getMainTable()
        
        r = ""
        
        #base attributes, always used
        kwargs = {"IndexName": 'record_type-index', "KeyConditionExpression": Key('record_type').eq(record_type)}

        #override from the parameter
        if( key_condition_kwargs is not None ):
            kwargs["KeyConditionExpression"] = key_condition_kwargs

        #if we just want certain attributes returned from the DynamoDB table
        if len(attribs) > 0:
            #similar to Javascript string join
            projection_expression = ', '.join(attribs)
            
            #add on to the kwargs
            kwargs["Select"] = 'SPECIFIC_ATTRIBUTES'
            kwargs["ProjectionExpression"] = projection_expression

        #now do the query now that the kwargs are established
        r = table.query(**kwargs)
        
        #KeyConditionExpression=Key('person_id').eq('abc123') & Key('record_type').eq('institution')
        
        return r

    def getScan(record_type, attribs=[]):
        table = db_core.getMainTable()

        r = ""

        #base attributes, always used
        kwargs = {"FilterExpression": Attr('record_type').eq(record_type)}
        
        #if we just want certain attributes returned from the DynamoDB table
        if len(attribs) > 0:
            #similar to Javascript string join
            projection_expression = ', '.join(attribs)

            kwargs["Select"] = 'SPECIFIC_ATTRIBUTES'
            kwargs["ProjectionExpression"] = projection_expression


        r = table.query(**kwargs)
        
        return r
