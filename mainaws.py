import os, pdb
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import BedrockEmbeddings  
from langchain_community.llms import Bedrock                
from pinecone import Pinecone
import boto3
from openai import AzureOpenAI
from dotenv import load_dotenv 
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx


# Load environment variables
load_dotenv()
# Initialize Azure OpenAI client
# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY1"),  
#     api_version="2024-02-01",
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT1")
# )

# Check if the user is authenticated
# def authenticate(username, password):
#     return username == st.secrets["auth"]["username"] and password == st.secrets["auth"]["password"]

# Display login form
# def login():
#     st.title("Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         if authenticate(username, password):
#             st.session_state["authenticated"] = True
#             st.experimental_rerun()
#         else:
#             st.error("Invalid username or password")



os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_KEY")
# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_KEY"))
index_name = "pdfs"
#index = pc.Index(index_name)


# Streamlit Configuration
st.set_page_config(page_title="PDF QA System")
st.title("Ask Questions About Your PDF")

# Function to initialize AWS Bedrock
def init_bedrock():
    """Initialize AWS Bedrock client"""
    return boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
#        aws_session_token=os.getenv("AWS_SESSION_TOKEN")  
    )

# Function to set up QA chain
def setup_qa_chain():
    try:
        # Initialize AWS Bedrock
        bedrock_runtime = init_bedrock()

        # Define Embeddings using Amazon Titan
        embeddings = BedrockEmbeddings(
            client=bedrock_runtime,
            model_id="amazon.titan-embed-text-v1"
        )

        # Set up Pinecone as a vector store
        vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

        

        # Define Claude LLM for RAG
        llm = Bedrock(
            client=bedrock_runtime,
            model_id="anthropic.claude-v2",
            model_kwargs={"temperature": 0, "max_tokens_to_sample": 1000}
        )

        # Create QA Retrieval Chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )

        # Store in session state
        st.session_state.qa_chain = qa_chain
        st.success("QA system initialized successfully!")

    except Exception as e:
        st.error(f"Error setting up QA system: {str(e)}")

# Check authentication
# if "authenticated" not in st.session_state:
#     st.session_state["authenticated"] = False

# if not st.session_state["authenticated"]:
#     login()

# Ensure QA Chain is initialized
if "qa_chain" not in st.session_state:
    with st.spinner("Initializing QA system..."):
        setup_qa_chain()

# User Input
question = st.text_input("Ask a question about your PDF:")

if question:
    if "qa_chain" not in st.session_state:
        st.error("QA system is not initialized. Please refresh the page.")
    else:
        try:
            with st.spinner("Generating answer..."):
                response = st.session_state.qa_chain({"query": question})
                st.write("### Answer:")
                st.write(response["result"])

                # Display Sources
                st.write("### Sources:")
                sources = response["source_documents"]
                for i, source in enumerate(sources):
                    st.write(f"Source {i+1}:")
                    st.write(source.page_content)
                    st.write("---")

        except Exception as e:
            st.error(f"Error generating answer: {str(e)}")
