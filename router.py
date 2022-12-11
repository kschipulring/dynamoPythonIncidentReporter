import json

from controllers.Incident import Incident
from controllers.Institution import Institution
from controllers.Person import Person
from controllers.Role import Role


def getData(param_id, controller, key_condition_kwargs=None, attribs=[]):
    outval = None

    #single, specific record
    if param_id is not None:
        outval = controller.get(param_id)
    else:
        #potentially many records
        outval = controller.getQuery(key_condition_kwargs, attribs)

    return outval


#determine what the larger overall function shall do, based on the HTTP endpoint
def route(event):

    # what gets returned by this method
    outval = ""
    
    # first get the HTTP method, whether it is GET or POST. Other kinds are problematic from browser.
    http_method = event["requestContext"]["http"]["method"]
    
    # simple op to get the base_endpoint and the param_id. 'None'... are the defaults to prevent system error
    base_endpoint, param_id, *_ = [e for e in event["rawPath"].split("/") if e] + [None, None]

    #two sets of routes, one based on get, other on post
    if http_method == "GET":
    
        """
        now do the actual routing for the GET endpoints.
        If the param_id is not populated, then call multiple records of that type.
        All records of that type shall be retrieved if no other parameters are presented.
        """
        if base_endpoint == "roles":
            outval = getData(param_id, Role())
        elif base_endpoint == "incidents":
            outval = getData(param_id, Incident())
        elif base_endpoint == "institutions":
            outval = getData(param_id, Institution())
        elif base_endpoint == "people":
            outval = getData(param_id, Person())
        else:
            outval = outval
    
    return outval
