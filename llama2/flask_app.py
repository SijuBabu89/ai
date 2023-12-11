from flask import Flask, request
from llama_cpp import llama_token_data

import llama2impl
import openai_impl
import pinecone_impl
import json

application = Flask(__name__)


@application.route('/')
def hello_world():
    return 'Hello world!'


@application.route('/code-extraction', methods=['POST'])
def extract_tabular_data():
    result = ""
    code_type = request.form.get('code_type')
    model = request.form.get('model')
    query = request.form.get('query')
    if code_type is not None:
        if model == "LLAMA_2":
            result = llama2impl.get_llama2_search_result(query)
            print(f'Below is the output for {model}')
            print(result)
        elif model == "OPEN_AI":
            result = openai_impl.get_openai_result(query).split('\n')
            print(f'Below is the output for {model}')
            print(result)
        else:
            result = []
            output = pinecone_impl.get_similarity_search_result(query)
            for document in output:
                result.append(document.page_content.split('\n'))
            print(f'Below is the output from vector database')
            print(result)
    api_response = {
        "model": model,
        "result": result,
        "query": query,
    }
    api_response.pop("Document", None)
    json_response = json.dumps(api_response)
    return json_response


if __name__ == '__main__':
    print("---- Into the main Function ----")
    application.run(debug=True, host='0.0.0.0', port=5004)
