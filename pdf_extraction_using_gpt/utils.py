#from langchain.llms import OpenAI
from langchain.llms import LlamaCpp
from pypdf import PdfReader
from langchain.llms.openai import OpenAI
import pandas as pd
import re
import replicate
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download


# Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Function to extract data from text
def extracted_data(pages_data):

    template = """Given below is a patient referral document. I want to extract all the following values : Patient FirstName, Patient LastName, Patient DOB, Patient   PhoneNumber, Patient  Secondaryphone,
        Patient Address , Patient City, Patient State, Patient Zip, Patient Email, Patient Primary Insurance, Patient Ethinicty, Patient Race, Patient PCP, 
        Referring Physician, MemberId and Groupnumber.
        
        {pages}"""    
        
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)

    #llm = OpenAI(temperature=.7)
    #full_response = llm(prompt_template.format(pages=pages_data))
    #print('*******************************************************************')
    #print(pages_data)
    #print('*******************************************************************')
    llm = get_llama2_llm()
    prompt = prompt_template.format(pages=pages_data)
    print(prompt)
    full_response = llm(prompt)
    #full_response = llm("Given is a referral document please give me the patient details and its demographics")
    #print(full_response)
    # The below code will be used when we want to use LLAMA 2 model,  we will use Replicate for hosting our model...

     #output = replicate.run('replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1',
     #input={"prompt":prompt_template.format(pages=pages_data) ,
     #"temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})

    # full_response = ''
    # for item in output:
    # full_response += item
    print('-----------------------------------------------------------------------------------------------------------------------')
    print('Full Response')
    print(full_response)
    print('-----------------------------------------------------------------------------------------------------------------------')
    return full_response


def get_llama2_llm():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
    #model_name_or_path =  "C://Users//sijus//.cache//huggingface//hub//models--TheBloke--Llama-2-13B-chat-GGML//snapshots//47d28ef5de4f3de523c421f325a2e4e039035bab"
    #model_basename = "llama-2-13b-chat.ggmlv3.q5_K_S.bin"  # the model is in bin format
    model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin"  # the model is in bin format
    model = ""
    model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)
    n_gpu_layers = 40  # Change this value based on your model and your GPU VRAM pool.
    n_batch = 256  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
    # Loading model,
    llm = LlamaCpp(
        model_path=model_path,
        max_tokens=256,
        n_batch=n_batch,
        callback_manager=callback_manager,
        n_ctx=2048,
        verbose=False,
    )
    #print(llm)
    return llm

# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list):
    #print(user_pdf_list)
    df = pd.DataFrame({'Invoice no.': pd.Series(dtype='str'),
                       'Description': pd.Series(dtype='str'),
                       'Quantity': pd.Series(dtype='str'),
                       'Date': pd.Series(dtype='str'),
                       'Unit price': pd.Series(dtype='str'),
                       'Amount': pd.Series(dtype='int'),
                       'Total': pd.Series(dtype='str'),
                       'Email': pd.Series(dtype='str'),
                       'Phone number': pd.Series(dtype='str'),
                       'Address': pd.Series(dtype='str')
                       })
    for filename in user_pdf_list:

        #print(filename)
        raw_data = get_pdf_text(filename)
        #print(raw_data)
        #print("extracted raw data")

        llm_extracted_data = extracted_data(raw_data)
        print("llm extracted data")
        print(llm_extracted_data)
        # Adding items to our list - Adding data & its metadata

        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)
        data_dict = ''
        if match:
            extracted_text = match.group(1)
            # Converting the extracted text to a dictionary
            data_dict = eval('{' + extracted_text + '}')
            print(data_dict)
        else:
            print("No match found.")

        df = df._append([data_dict], ignore_index=True)
        print("********************DONE***************")
        # df=df.append(save_to_dataframe(llm_extracted_data), ignore_index=True)

    df.head()
    return df
