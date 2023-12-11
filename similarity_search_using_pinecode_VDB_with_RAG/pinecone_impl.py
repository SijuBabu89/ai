from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pinecone
import os
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

index_name = "insurance-list"  # put in the name of your pinecone index here
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')


def init_pinecone():
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
    #PINECONE_API_KEY: str = os.environ.get('PINECONE_API_KEY', 'd50e429b-331d-409f-876b-313c61ad30a0')
    PINECONE_API_ENV: str = os.environ.get('PINECONE_API_ENV', 'asia-southeast1-gcp-free')
    # initialize pinecone
    pinecone.init(
        api_key='d50e429b-331d-409f-876b-313c61ad30a0',  # find at app.pinecone.io
        environment='asia-southeast1-gcp-free'
        #environment=PINECONE_API_ENV  # next to api key in console
    )


def get_docs():
    init_pinecone()
    docs = Pinecone.from_existing_index(index_name, embeddings)
    return docs


def get_similarity_search_result(query):
    docsearch = get_docs()
    doc_result = docsearch.similarity_search(query)
    # print('_________________________________ PINECONE SIMILARITY SEARCH RESULT _________________________________')
    # print(doc_result)
    # print('____________________________________________ END ____________________________________________________')
    return doc_result


def upload_document(file_path):
    init_pinecone()
    loader = PyPDFLoader(file_path)
    data = loader.load()
    #text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    #docs = text_splitter.split_documents(data)
    split_output = []
    for document in data:
        lines = document.page_content.split('\n')
        for line in lines:
            split_output.append(line)
    #docsearch = Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)
    docsearch = Pinecone.from_texts(split_output, embeddings, index_name=index_name)
    docsResult = Pinecone.from_existing_index(index_name, embeddings)
    # print(len(docsearch))
    return len(docsearch)


def check_index(index_nam):
    init_pinecone()
    result = False
    available_pinecone_index = pinecone.list_indexes()
    if len(available_pinecone_index) > 0:
        if index_nam in available_pinecone_index:
            result = True
    return result


def create_index(index_nam):
    if check_index(index_nam):
        print('Index Available')
    else:
        pinecone.create_index(index_nam, dimension=384 , metric="cosine", pods=1, pod_type="s1.x1")

def delete_index(delete_index):
    if check_index(delete_index):
        pinecone.delete_index(delete_index)
    else:
        print('Index Not Available')


def upload_document(doc_name):
    init_pinecone()
    loader = PyPDFLoader("files/" + doc_name)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(data)
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    index_name = "insurance-list"  # put in the name of your pinecone index here
    docsearch = Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)
    docsResult = Pinecone.from_existing_index(index_name, embeddings)
    print(docsResult)

def get_docs():
    init_pinecone()
    docs = Pinecone.from_existing_index("insurance-list", embeddings)
    # print(docs)
    return docs


def get_similarity_search_result(query):
    docsearch = get_docs()
    doc_result = docsearch.similarity_search(query)
    print('_________________________________ PINECONE SIMILARITY SEARCH RESULT _________________________________')
    print(doc_result[0].page_content)
    print('____________________________________________ END ____________________________________________________')
    return doc_result[0].page_content
def init_openai():
    os.environ['OPENAI_API_KEY'] = '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'
    #os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

def get_openai_result(query):
    query = "What is the insurance name for "+query+" please return only the result"
    init_openai()
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1)
    vector_store = get_docs()
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 5})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    answer = chain.run(query)
    print('_____________________________ OPEN AI RESULT _______________________________')
    print(answer)
    print('__________________________________ END _____________________________________')
    return answer


#get_openai_result("BCBS")
#get_similarity_search_result("BCBS ")
#upload_document("ECWInsuranceNameList.pdf")
#create_index(index_name)
