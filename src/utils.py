import json
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)


class Utils:
    def read_json(self, file_path):
        """Reads a JSON file and returns its content as a dictionary."""
        with open(file_path, 'r') as file:
            return json.load(file)

class Embeddings:
    
    def openai_embedding(self, data, model="text-embedding-3-large"):
        openaiclient = OpenAI()
        return openaiclient.embeddings.create(
            input = data, 
            model=model, 
            dimensions=1536
            ).data[0].embedding
    
    def hf_sentence_transformers_embedding(self, sentences):
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embeddings = model.encode(sentences)

        return embeddings[0]

    def pinecone_embeddings(self, data):
        assert isinstance(data, list), "Data must be a list of dictionaries."
        print('Converting the child tags into numerical vectors that Pinecone can index')
        embeddings = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[d['child_tag'] for d in data],
            parameters={"input_type": "passage", "truncate": "END"}
        )
        print('Embedding generation done')


        return embeddings
    
    def pinecone_query_embeddings(self, query):
        # Convert the query into a numerical vector that Pinecone can search with
        query_embedding = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[query],
            parameters={
                "input_type": "query"
            }
        )

        return query_embedding

class QueryVector:
    def __init__(self):
        self.index_name = "tags"
        self.index = pc.Index(self.index_name)
        self.embed = Embeddings()

    def query_vector(self, query):
        # Generate embeddings for the query
        pinecone_query_embeddings_results = self.embed.pinecone_query_embeddings(query)

        # Search the index for the three most similar vectors
        results = self.index.query(
            namespace="re-tags",
            vector=pinecone_query_embeddings_results[0].values,
            top_k=1,
            include_values=False,
            include_metadata=True
        )
        # check if the parent tag is in the results
        parent_tag = {'parent_tag':results['matches'][0]['metadata'].get('parent_tag',None)}

        return parent_tag