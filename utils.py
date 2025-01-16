import json
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

openaiclient = OpenAI()

class Utils:
    def read_json(self, file_path):
        """Reads a JSON file and returns its content as a dictionary."""
        with open(file_path, 'r') as file:
            return json.load(file)

class Embeddings:
    
    def openai_embedding(self, data, model="text-embedding-3-large"):
        
        return openaiclient.embeddings.create(
            input = data, 
            model=model, 
            dimensions=1536
            ).data[0].embedding
    
    def hf_sentence_transformers_embedding(self, sentences):
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embeddings = model.encode(sentences)

        return embeddings[0]
