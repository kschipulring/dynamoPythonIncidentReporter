import json

import person
import role
import incident
import institution

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
        param_id = ""
    else:
        #but if there is one
        param_id = path_parameters.get("proxy", "")

    
    #two sets of routes, one based on get, other on post
    if http_method == "GET":
    
        #now do the actual routing for the GET endpoints
        if base_endpoint == 'getPerson':
            outval = person.get(param_id)
            
        elif base_endpoint == "getRole":
            outval = role.get(param_id)
            
        elif base_endpoint == "getIncident":
            outval = "call the getIncident function with " + param_id
         
        elif base_endpoint == "getInstitution":
            outval = "call the getIncident function with " + param_id
            
        elif base_endpoint == "getPeople":
            
            #outval = person.getScan(["last_name", "first_name"])
            outval = person.getQuery()
        else:
            outval = outval
    
    return outval
