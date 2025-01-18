from pinecone import Pinecone, ServerlessSpec
import time
import os
import json
from dotenv import load_dotenv

from src.utils import Utils, Embeddings

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)
utilities = Utils()
embed = Embeddings()

data = utilities.read_json('./test/data.json')

# Create Index
index_name = "tags"
# pc.delete_index(index_name)

existing_indexes = [
    index_info["name"] for index_info in pc.list_indexes()
]

print('existing indexes: ', existing_indexes)

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region='us-east-1'
            )
        )
    while not pc.describe_index(index_name).status['ready']:
        print('waiting for index to be initialized')
        time.sleep(1)

index = pc.Index(index_name)


embeddings = embed.pinecone_embeddings(data)

# embeddings = embed.append(embed.hf_sentence_transformers_embedding([v[0]]))

vectors = []
for d, e in zip(data, embeddings):
    vectors.append({
        "id": d['id'],
        "values": e['values'],
        "metadata": {"parent_tag": d["parent_tag"]}
    })

print(f"Upserting {len(vectors)} data points")
index.upsert(
    vectors=vectors,
    namespace="re-tags"
)


# convert_to_vectors = [i['child_tag'] for i in data]

# print(convert_to_vectors)
# convert_to_vectors = convert_to_vectors[0:2]

# new_data = []
# data = data[0:1]
# n=0
# for k,v in data.items():
#     n+=1
#     new_data.append({"id":n, "parent_tag":k, "child_tag":v[0]})

# with open('new_data.json', 'w') as json_file:
#     json.dump(new_data, json_file, indent=2)


# for i in new_data:
#     print(i)
# print(new_data)

# documents = []
# metadata = []
# ids = []
# embeddings = []
# n=0
# for k,v in data.items():
#     n+=1
#     documents.append(v[0])
#     metadata.append({"parent_tag":k})
#     ids.append(k)
#     print("Creating embeddings. Item number: ", n+1)
#     embeddings.append(embed.hf_sentence_transformers_embedding([v[0]]))
#     # embeddings.append(embed.openai_embedding(v[0]))
  

# print(embeddings)
