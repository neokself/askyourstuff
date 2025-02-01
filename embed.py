from PyPDF2 import PdfReader
from openai import AzureOpenAI
import pinecone
import os,pdb
from dotenv import load_dotenv 
from pinecone import Pinecone, ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
# Initialize Azure OpenAI client
azureapikey=os.getenv("AZURE_OPENAI_API_KEY1")
azureendpoint=os.getenv("AZURE_OPENAI_ENDPOINT1")

#pdb.set_trace()
# Initialize Azure OpenAI client
client = AzureOpenAI(
  api_key = "a333d0e832bd4e0c8624a362a7ff66ce",  
  api_version = "2024-02-01",
  azure_endpoint = "https://kkai.openai.azure.com/"
)

# Initialize Pinecone
pc=Pinecone(api_key=os.getenv("PINECONE_KEY"))

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Chunk text
# def chunk_text(text, chunk_size=500):
#     words = text.split()
#     chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
#     return chunks

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Optimal size based on LLM
    chunk_overlap=200,  # Ensures context isn't lost
    length_function=len
)

# Generate embeddings using Azure OpenAI
def generate_embeddings(chunks):
    embeddings = []
   # pdb.set_trace()
    name=os.getenv("AZURE_OPENAI_EMBED_NAME")
    for chunk in chunks:
        response = client.embeddings.create(
            input=chunk,
            model=name
        )

    #    pdb.set_trace()
        # Access the embedding from the response
        embedding = response.data[0].embedding
        embeddings.append(embedding)
    return embeddings

# Upload to Pinecone
def upload_pdf_to_pinecone(pdf_path):
 
    index_name="pdfs"   
    index = pc.Index(index_name)
#    pdb.set_trace()
    # Extract, chunk, and generate embeddings
    text = extract_text_from_pdf(pdf_path)
    filename=os.path.basename(pdf_path)
    
#    pdb.set_trace()
#    chunks = chunk_text(text)
    chunks = text_splitter.split_text(text)

    
#    pdb.set_trace()
    embeddings = generate_embeddings(chunks)

    # Upload embeddings
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
    #    pdb.set_trace()        
        index.upsert([(f"{filename}-chunk-{i}", embedding, {"text": chunk})])

    print(f"Uploaded {len(chunks)} chunks from {pdf_path} to Pinecone.")

# Function to process all PDFs in a directory (recursively)
def process_pdfs_in_directory(directory):
    pdf_files = set()  # Use a set to avoid duplicates
    print(f"Scanning directory: {directory}")
    
    # Walk through directory and subdirectories
    for root, _, files in os.walk(directory, followlinks=False):
        print(f"Scanning subdirectory: {root}")
#        pdb.set_trace()
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                if file_path in pdf_files:
                    print(f"Duplicate file found: {file_path}")
                else:
                    pdf_files.add(file_path)
                    print(f"Found PDF: {file_path}")

    print(f"Found {len(pdf_files)} unique PDFs in {directory}...")

    for pdf_path in pdf_files:
        try:
            print(f"Processing: {pdf_path}")
            upload_pdf_to_pinecone(pdf_path)    
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")

# Main execution
if __name__ == "__main__":
    directory_path = os.getenv("DIR_PATH")

    if os.path.exists(directory_path):
        print("Starting PDF processing...")
        process_pdfs_in_directory(directory_path)
    else:
        print("Invalid directory path. Please check and try again.")