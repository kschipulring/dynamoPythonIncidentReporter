import json

import router

def lambda_handler(event, context):
    
    #return event["requestContext"]["routeKey"]
    return router.route( event )

