from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pinecone
import os

index_name = "langchainpinecone"  # put in the name of your pinecone index here
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')


def init_pinecone():
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
    PINECONE_API_KEY: str = os.environ.get('PINECONE_API_KEY', 'd50e429b-331d-409f-876b-313c61ad30a0')
    PINECONE_API_ENV: str = os.environ.get('PINECONE_API_ENV', 'asia-southeast1-gcp-free')
    # initialize pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment=PINECONE_API_ENV  # next to api key in console
    )


def get_docs():
    init_pinecone()
    docs = Pinecone.from_existing_index(index_name, embeddings)
    return docs


def get_similarity_search_result(query):
    docsearch = get_docs()
    doc_result = docsearch.similarity_search(query)
    #print('_________________________________ PINECONE SIMILARITY SEARCH RESULT _________________________________')
    #print(doc_result)
    #print('____________________________________________ END ____________________________________________________')
    return doc_result


def upload_document(file_path):
    init_pinecone()
    loader = PyPDFLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(data)
    docsearch = Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)
    #print(len(docsearch))
    return len(docsearch)
