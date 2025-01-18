import chromadb
from chromadb.config import Settings


# from chromadb.config import Settings

# # Initialize the ChromaDB client
client = chromadb.Client()
client = chromadb.PersistentClient(path="./chroma", settings=Settings(allow_reset=True))
client.reset()

from utils import Utils, Embeddings

# Create a collection to store vectors
collection = client.create_collection("tag_store")

utilities = Utils()
embed = Embeddings()

data = utilities.read_json('./data.json')

documents = []
metadata = []
ids = []
embeddings = []
n=0
for k,v in data.items():
    n+=1
    documents.append(v[0])
    metadata.append({"parent_tag":k})
    ids.append(k)
    print("Creating embeddings. Item number: ", n+1)
    embeddings.append(embed.hf_sentence_transformers_embedding([v[0]]))
    # embeddings.append(embed.openai_embedding(v[0]))
    
print('documents:', documents, '\n\n metadata:', metadata, "\n\nids:", ids)
collection.add(
    documents=documents,
    metadatas=metadata,
    embeddings=embeddings,
    ids=ids
)
