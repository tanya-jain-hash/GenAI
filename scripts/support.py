import os
from dotenv import load_dotenv
load_dotenv()

from pinecone import Pinecone
from pinecone import ServerlessSpec

from ollama import chat
from ollama import ChatResponse
from sentence_transformers import SentenceTransformer

pinecone_api_key  = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

index_name = "logistics-faq"
index = pc.Index(index_name)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')

def get_content(query)->list:
        """Useful to generate answers from retrived chunks of documents"""
        query_embedding = model.encode(query).tolist()

        print("===========Retrieving content===========")

        results = index.query(
            namespace="douments",
            vector=query_embedding,
            top_k=3,
            include_values=False,
            include_metadata=True
        )

        return [match["metadata"]["text"].replace("\t"," ").replace("\n"," ") for match in results["matches"]]

def get_response(query):
    content = get_content(query)
    response: ChatResponse = chat(model="BahaSlama/llama3.1-finetuned:latest", messages=[
    {
        'role': 'user',
        'content': f"Answer user query from provided content: \n query:{query}, content: {content}, Answer:",
    },
    ])
    # or access fields directly from the response object
    return response.message.content

    