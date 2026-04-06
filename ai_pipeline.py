from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import litellm
from groq import Groq
import cohere
import chromadb
from sentence_transformers import SentenceTransformer
import tiktoken
from llama_index.core import VectorStoreIndex

def build_pipeline():
    # Groq for fast inference
    groq_client = Groq()

    # Cohere for embeddings
    co = cohere.Client()

    # ChromaDB as vector store
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection("docs")

    # Sentence transformers for local embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # LiteLLM as unified gateway
    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )

    return response
