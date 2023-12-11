from flask import Flask, request, abort
import json
from pinecone_impl import *
from flask_restful import Api

app = Flask(__name__)
api = Api(app, "/insurance")


@app.route('/')
def ecw_insurance_mapping():
    return 'ECW Insurance Mapping!'


@app.route('/similarity-search', methods=['POST'])
def similarity_search():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    insurance_result = ''
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    print('-------------------------------------------------------------------------------------')
    print('REQUEST : ')
    print(request)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST FORM : ')
    print(request.form)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST HEADERS : ')
    print(request.headers)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST ARGS : ')
    print(request.args)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST JSON : ')
    print(request.get_json())
    print('-------------------------------------------------------------------------------------')
    print('AUTHENTICATION')
    print(request.authorization)
    print('-------------------------------------------------------------------------------------')

    insurance = request.get_json().get('insurance')
    plan_name = request.get_json().get('plan_name')
    plan_name = "" if plan_name is None else plan_name
    insurance = "" if insurance is None else insurance
    query = insurance + ' ' + plan_name
    if insurance is not None:
        result = get_similarity_search_result(query)
        # Split the string into a list of elements based on the newline character '\n'
        data_list = result.split('\n')

        # Convert the list to JSON format
        json_output = json.dumps(data_list)

        # Load the JSON string back to a Python object
        parsed_json = json.loads(json_output)

        # Extract the first element
        first_element = parsed_json[0]
        # Parse the JSON string into a Python dictionary
        # insurance_result = json.loads(result)
    print(first_element)
    api_response = {
        "Output": first_element
    }
    return api_response


@app.route('/ll_search', methods=['POST'])
def llm_search():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    insurance = request.get_json().get('insurance')
    plan_name = request.get_json().get('plan_name')
    plan_name = "" if plan_name is None else plan_name
    insurance = "" if insurance is None else insurance
    query = insurance + ' ' + plan_name
    if insurance is not None:
        result = get_openai_result(query)
        # Parse the JSON string into a Python dictionary
        #insurance_result = json.loads(result)
    api_response = {
        "Output": result
    }
    return api_response


if __name__ == '__main__':
    print("---- Into the main Function ----")
    app.run(debug=True, host='0.0.0.0', port=5008)
