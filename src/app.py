import sys
sys.path.insert(0, '.')

import json
import os
from utils import Embeddings
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()
embed = Embeddings()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "tags"
index = pc.Index(index_name)

def lambda_handler(event, context):

    # Extract query from the POST request body
    body = json.loads(event['body'])
    query = body.get('query', '')

    if not query:
        return {
            'statusCode': 400,
            'body': json.dumps('Query parameter is missing.')
        }

    # Generate embeddings for the query
    pinecone_query_embeddings_results = embed.pinecone_query_embeddings(query)

    # Search the index for the three most similar vectors
    results = index.query(
        namespace="re-tags",
        vector=pinecone_query_embeddings_results[0].values,
        top_k=1,
        include_values=False,
        include_metadata=True
    )
    parent_tag = {'parent_tag':results['matches'][0]['metadata']['parent_tag']}

    return {
        'statusCode': 200,
        'body': json.dumps(parent_tag)
    }