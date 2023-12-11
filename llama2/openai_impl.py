from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

import pinecone_impl
import os


def init_openai():
    os.environ['OPENAI_API_KEY'] = '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'


def get_openai_result(query):
    init_openai()
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1)
    vector_store = pinecone_impl.get_docs()
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 5})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    answer = chain.run(query)
    #print('_____________________________ OPEN AI RESULT _______________________________')
    #print(answer)
    #print('__________________________________ END _____________________________________')
    return answer
