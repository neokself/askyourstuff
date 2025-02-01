from PyPDF2 import PdfReader
from openai import AzureOpenAI
import pinecone
import os
import pdb



# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",  # Use the latest supported version
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Initialize Pinecone
pinecone.init(api_key=os.getenv(os.getenv("PINECONE_KEY")))

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Chunk text
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Generate embeddings using Azure OpenAI
def generate_embeddings(chunks, deployment_name=name):
    embeddings = []
    pdb.set_trace()    
    for chunk in chunks:
        response = client.embeddings.create(
            input=chunk,
            model=os.getenv("AZURE_OPENAI_DEPLOYENT_NAME")  # Use your Azure OpenAI deployment name
        )
        pdb.set_trace()
        # Access the embedding from the response
        embedding = response.data[0].embedding
        embeddings.append(embedding)
    return embeddings


# Upload to Pinecone
def upload_pdf_to_pinecone(pdf_path, index_name="pdfs", deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")):
    # Create or connect to an index
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=1536)  # Azure OpenAI embeddings have 1536 dimensions

    index = pinecone.Index(index_name)

    # Extract, chunk, and generate embeddings
    text = extract_text_from_pdf(pdf_path)

#    chunks = chunk_text(text)
#    embeddings = generate_embeddings(chunks, deployment_name)
    pdb.set_trace()
    chunks = ["This is a test chunk."]
    embeddings = generate_embeddings(chunks,os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"))
    print(embeddings)
    pdb.set_trace() 
    # Upload embeddings
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        index.upsert([(f"chunk-{i}", embedding, {"text": chunk})])

    print(f"Uploaded {len(chunks)} chunks from {pdf_path} to Pinecone.")


# Function to process all PDFs in a directory (recursively)
def process_pdfs_in_directory(directory):
    pdf_files = []

    # Walk through directory and subdirectories
    for root, _, files in os.walk(directory, followlinks=False):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    pdb.set_trace() 
    print(f"Found {len(pdf_files)} PDFs in {directory}...")
    pdb.set_trace() 
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
        process_pdfs_in_directory(directory_path)
    else:
        print("Invalid directory path. Please check and try again.")
