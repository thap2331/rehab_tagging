import chromadb

client = chromadb.Client()
client = chromadb.PersistentClient(path="./chroma")


from utils import Utils, Embeddings

# Create a collection to store vectors
collection = client.get_collection("tag_store")
embed = Embeddings()

print('chroma client:',client.heartbeat())

query = 'bought from lowes for floor $5000'
# query_vector = embed.openai_embedding(query.lower())
query_vector = embed.hf_sentence_transformers_embedding([query.lower()])

results = collection.query(
    query_embeddings=[query_vector],
    n_results=3  # Number of nearest neighbors to retrieve
)


print(results)
