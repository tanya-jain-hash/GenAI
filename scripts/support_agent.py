import os
import langchain
from langchain_community.document_loaders import PyPDFLoader

from pinecone import Pinecone
from pinecone import ServerlessSpec

from sentence_transformers import SentenceTransformer

import ollama
from crewai import Agent, Crew, Task
from crewai import LLM
from crewai.tools import tool

from ollama import chat
from ollama import ChatResponse

from crewai.flow.flow import Flow, listen, start
import asyncio

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter

pinecone_api_key  = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

index_name = "logistics-faq"

pc.delete_index(index_name)
pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)


model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')

documents_path = os.path.join(os.getcwd(),"documents")
print(documents_path)

def store_embeddings():
    idx = 1
    for file in os.listdir("documents"):
        f = open(os.path.join(documents_path, file))
        text = f.read()
        # print(text)
        text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("--","Pair")])
        splits = text_splitter.split_text(text)
        print(len(splits))
        embeddings =  model.encode([text]) 
        vectors = [{"id":str(idx),"values":embeddings[0],"metadata": {'text': text}}]
        index.upsert(vectors=vectors,namespace="douments")
        idx+=1


store_embeddings()

def initialise_ollama(model_name="tinyllama:1.1b"):
    ollama.pull(model_name)
    print(ollama.list())
# initialise_ollama()


llm = LLM(
    model="ollama/tinyllama:1.1b",
    base_url="http://localhost:11434"
)

query = "How long will it take for my package to arrive?"


class ExampleFlow(Flow):
    model = llm
    @start()
    def get_content(self)->list:
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

    @listen(get_content)
    def get_response(self, get_content):
        response: ChatResponse = chat(model="tinyllama:1.1b", messages=[
        {
            'role': 'user',
            'content': f"Answer user query from provided content: \n query:{query}, content: {get_content}, Answer:",
        },
        ])
        # or access fields directly from the response object
        return response.message.content

flow = ExampleFlow()
# flow.plot()
result = flow.kickoff_async()

print(f"Generated fun fact: {result}")