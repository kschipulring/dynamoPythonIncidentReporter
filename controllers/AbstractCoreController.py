from abc import ABC, abstractmethod

import boto3
from boto3.dynamodb.conditions import Key, Attr

#import the connection to the main database
import ddb.db_core as db_core

class AbstractCoreController(ABC):

    def __init__(self, record_type):
        self.table = db_core.getMainTable()
        
        self.record_type = record_type
        
        super().__init__()

    #just one record. Optional third parameter for when you only want certain attributes
    def get(self, id, attribs_returned=[]):
        r = ""

        #the main index is the record type and also an id
        kwargs = {"Key": {'record_type': self.record_type, 'id': id}}
        
        #if we just want certain attributes returned from DynamoDB
        if len(attribs_returned) > 0:
            kwargs["AttributesToGet"] = attribs_returned

        r = self.table.get_item(**kwargs)

        return r


    #multiple record QUERY of a particular record_type
    def getQuery(self, filter_expression_kwargs=None, attribs=[]):

        r = ""
        
        #base attributes, always used
        kwargs = {"KeyConditionExpression": Key('record_type').eq(self.record_type)}

        #override from the parameter
        if( filter_expression_kwargs is not None ):
            #something like: kwargs["FilterExpression"] = Attr('i_id').eq("12345")
            kwargs["KeyConditionExpression"] = filter_expression_kwargs

        #if we just want certain attributes returned from the DynamoDB table
        if len(attribs) > 0:
            #similar to Javascript string join
            projection_expression = ', '.join(attribs)
            
            #add on to the kwargs
            kwargs["Select"] = 'SPECIFIC_ATTRIBUTES'
            kwargs["ProjectionExpression"] = projection_expression

        #now do the query now that the kwargs are established
        r = self.table.query(**kwargs)
        
        return r

    def getScan(record_type, attribs=[]):
        table = db_core.getMainTable()

        r = ""

        #base attributes, always used
        kwargs = {"FilterExpression": Attr('record_type').eq(self.record_type)}
        
        #if we just want certain attributes returned from the DynamoDB table
        if len(attribs) > 0:
            #similar to Javascript string join
            projection_expression = ', '.join(attribs)

            kwargs["Select"] = 'SPECIFIC_ATTRIBUTES'
            kwargs["ProjectionExpression"] = projection_expression


        r = table.query(**kwargs)
        
        return r
