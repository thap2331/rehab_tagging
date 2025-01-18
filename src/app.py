import sys
sys.path.insert(0, '.')

import json
from utils import QueryVector
def lambda_handler(event, context):

    # Extract query from the POST request body
    body = json.loads(event['body'])
    query = body.get('query', '')

    if not query:
        return {
            'statusCode': 400,
            'body': json.dumps('Query parameter is missing.')
        }

    query_vector = QueryVector()
    parent_tag = query_vector.query_vector(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(parent_tag)
    }