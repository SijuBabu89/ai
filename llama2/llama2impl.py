from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download
from langchain.chains.question_answering import load_qa_chain
import pinecone_impl


def get_llama2_llm():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
    model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin"  # the model is in bin format
    model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)
    n_gpu_layers = 40  # Change this value based on your model and your GPU VRAM pool.
    n_batch = 256  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
    # Loading model,
    llm = LlamaCpp(
        model_path=model_path,
        max_tokens=256,
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        callback_manager=callback_manager,
        n_ctx=1024,
        verbose=False,
    )
    return llm


def get_llama2_search_result(query):
    chain = load_qa_chain(get_llama2_llm(), chain_type="stuff")
    #docs =  pinecone_impl.get_docs()
    #print('________________________________________________________')
    #print(docs)
    #print('##########################################################')
    docs = pinecone_impl.get_similarity_search_result(query)
    #print('__________________________________ LLAMA 2 RESULTS _________________________________')
    # print(docs)
    result = chain.run(input_documents=docs, question=query)
    #print('_______________________________________ END _________________________________________')
    return result
