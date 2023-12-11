from langchain.document_loaders import PyPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from sentence_transformers import SentenceTransformer
from langchain.chains.question_answering import load_qa_chain
import pinecone_impl
import os

#loader = OnlinePDFLoader("https://wolfpaulus.com/wp-content/uploads/2017/05/field-guide-to-data-science.pdf")
#loader = PyPDFLoader("files/The-Field-Guide-to-Data-Science.pdf")
#loader = PyPDFLoader("/content/The-Field-Guide-to-Data-Science.pdf")
#data = loader.load()
#data
#print(data)
#text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
#docs=text_splitter.split_documents(data)
#len(docs)
#print(docs[0])
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', 'd50e429b-331d-409f-876b-313c61ad30a0')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'asia-southeast1-gcp-free')
embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
#initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "langchainpinecone" # put in the name of your pinecone index here
docsearch = Pinecone.from_existing_index(index_name, embeddings)
query="What are examples of good data science teams?"
docs=docsearch.similarity_search(query)
print(docs)
print("Done")
