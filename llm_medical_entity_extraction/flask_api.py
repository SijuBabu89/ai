from flask import Flask, request
from medical_entity_code_extraction import extract_entity, extract_diseases

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/medical-entity', methods=['POST'])
def extract_medical_entity():
    model = request.form.get('model')
    print("model : " + model)
    medical_notes = request.form.get('notes')
    if model is not None:
        result = extract_entity(model, medical_notes)
        result = result.split('\n')
        result = ','.join(result)
        print(result)
    api_response = {
        "Output": result
    }
    return api_response


@app.route('/medical-disease', methods=['POST'])
def extract_medical_disease():
    model = request.form.get('model')
    print("model : " + model)
    medical_notes = request.form.get('notes')
    if model is not None:
        result = extract_diseases(model, medical_notes)
        result = result.split('\n')
        result = ','.join(result)
    api_response = {
        "Output": result
    }
    return api_response

if __name__ == '__main__':
    print("---- Into the main Function ----")
    app.run(debug=True, host='0.0.0.0', port=5007)
