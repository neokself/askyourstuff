import os, pdb
import pinecone
from pinecone import Pinecone
from dotenv import load_dotenv 


load_dotenv()
# Initialize Pinecone
pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_KEY"))
index_name = "pdfs"  # Your Pinecone index name
index = pc.Index(index_name)

pdb.set_trace()
# Delete all vectors from the index
index.delete(delete_all=True)

print("Index cleared successfully!")
