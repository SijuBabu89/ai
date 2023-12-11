from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain import PromptTemplate
import pinecone
import os
from datetime import datetime
from langchain.memory import ConversationBufferMemory

model_name = 'text-embedding-ada-002'

embeddings = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=os.environ.get('OPENAI_API_KEY'),
)

pinecone.init(
    api_key=os.environ.get('PINECONE_API_KEY'),
    environment='gcp-starter',
)
index = pinecone.Index('vectordb')
vectorstore = Pinecone(
    index=index,
    embedding_function=embeddings.embed_query,
    text_key='text',
)

def get_response(instruction, query):
    """
    This function takes in an instruction and a query, and returns a response and a list of results.
    instruction: str
    query: str
    Returns: str, list
    """
    results = vectorstore.similarity_search(query, k=5)

    llm = ChatOpenAI(
        openai_api_key=os.environ.get('OPENAI_API_KEY'),
        model_name='gpt-3.5-turbo',
        temperature=0.0,
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=vectorstore.as_retriever(),
    )

    t1 = datetime.now()
    query = str(instruction) + str(query)
    response = qa.run(query)
    t2 = datetime.now()
    print("Elapsed time for querying the result using LLM",  (t2-t1).total_seconds())
    return response, results
    
