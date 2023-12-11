from langchain.document_loaders import PyPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import os

loader = PyPDFLoader("files/icd10cm-tabular.pdf")
data = loader.load()
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs=text_splitter.split_documents(data)
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
docsearch=Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)

docsResult = Pinecone.from_existing_index(index_name, embeddings)
print(len(docsResult))