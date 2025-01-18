import json
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from pinecone.grpc import PineconeGRPC as Pinecone
from dotenv import load_dotenv
import os
from utils import Utils, Embeddings


load_dotenv()
embed = Embeddings()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define your query
query = "$250 for paint"

# Convert the query into a numerical vector that Pinecone can search with
# query_embedding = pc.inference.embed(
#     model="multilingual-e5-large",
#     inputs=[query],
#     parameters={
#         "input_type": "query"
#     }
# )

pinecone_query_embeddings_results = embed.pinecone_query_embeddings(query)
index_name = "tags"
index = pc.Index(index_name)


# Search the index for the three most similar vectors
results = index.query(
    namespace="re-tags",
    vector=pinecone_query_embeddings_results[0].values,
    top_k=3,
    include_values=False,
    include_metadata=True
)

print(results)


# import chromadb

# client = chromadb.Client()
# client = chromadb.PersistentClient(path="./chroma")


# from utils import Utils, Embeddings

# # Create a collection to store vectors
# collection = client.get_collection("tag_store")
# embed = Embeddings()

# print('chroma client:',client.heartbeat())

# query = 'bought from lowes for floor $5000'
# # query_vector = embed.openai_embedding(query.lower())
# query_vector = embed.hf_sentence_transformers_embedding([query.lower()])

# results = collection.query(
#     query_embeddings=[query_vector],
#     n_results=3  # Number of nearest neighbors to retrieve
# )


# print(results)
