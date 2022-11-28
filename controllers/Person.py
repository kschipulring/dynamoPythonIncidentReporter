from controllers.AbstractCoreController import AbstractCoreController

class Person(AbstractCoreController):

    #just one person. Optional second parameter for when you only want certain attributes
    def get(self, id, attribs_returned=[]):
        r = ""

        """
        in spite of the possibility that the record type may be something other
        than a person, 'person_id' is still a primary key
        """
        kwargs = {"Key": {'person_id': id, 'record_type': "person"}}
        
        #if we just want certain attributes returned from DynamoDB
        if len(attribs_returned) > 0:
            kwargs["AttributesToGet"] = attribs_returned

        r = self.table.get_item(**kwargs)

        return r

    #multiple people. Optional second parameter for when you only want certain attributes
    def getQuery(self, key_condition_kwargs=None, attribs=[]):
        return super().getQuery("person", key_condition_kwargs, attribs)

    #multiple people SCAN
    def getScan(attribs=[]):
        return super().getScan("person", attribs)
