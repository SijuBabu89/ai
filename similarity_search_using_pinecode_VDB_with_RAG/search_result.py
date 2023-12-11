#import llama2impl
#import openai_impl
import pinecone_impl


#file_path = "files/icd10cm-tabular.pdf"
# query = "What are the icd code for anaphylactic shock"
# result = pinecone_impl.get_similarity_search_result(query)
# print(result[0].page_content)
# openai_impl.get_openai_result(query)
# llama2impl.get_llama2_search_result(query)
# llama2impl.get_llama2_search_result(query)

def similarity_search(query):
    print(" Result ")
    result = pinecone_impl.get_similarity_search_result(query)
    print(" Result ")
    print(result[0].page_content)
    return result[0].page_content

similarity_search("AETNA")