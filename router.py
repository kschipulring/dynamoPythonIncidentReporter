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

    #what gets returned by this method
    outval = ""
    
    #first get the HTTP method, whether it is GET or POST. Other kinds are problematic from browser.
    http_method = event["requestContext"]["http"]["method"]
    
    #just get the base endpoint
    base_endpoint = event["routeKey"].replace(http_method + " ", "").replace("/", "").replace("{proxy}", "")
    
    #find out if this route has an optional parameter. '0' means it does not.
    path_parameters = event.get("pathParameters", 0)
    
    #if this is a top level endpoint, then there is no meaningful param_id
    if not path_parameters:
        param_id = None
    else:
        #but if there is one
        param_id = path_parameters.get("proxy", "")

    
    #two sets of routes, one based on get, other on post
    if http_method == "GET":
    
        #now do the actual routing for the GET endpoints
        if base_endpoint == "getRoles":
            outval = getData(param_id, Role())
        elif base_endpoint == "getIncidents":
            outval = getData(param_id, Incident())
        elif base_endpoint == "getInstitutions":
            outval = getData(param_id, Institution())
        elif base_endpoint == "getPeople":
            outval = getData(param_id, Person())
        else:
            outval = outval
    
    return outval
