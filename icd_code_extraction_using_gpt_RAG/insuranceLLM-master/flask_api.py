from insuranceLLM import api
from flask import Flask, request, abort
import json
from time import process_time
from datetime import datetime

sample_result = '''
{
  "Diseases": [
    {
      "Disease": "Dyspepsia",
      "Laterality": "Not specified",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Not specified",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Dyspepsia>"
    },
    {
      "Disease": "Esophageal Ulcer",
      "Laterality": "Not specified",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Not specified",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Esophageal Ulcer>"
    },
    {
      "Disease": "Overweight",
      "Laterality": "Not specified",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Not specified",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Overweight>"
    },
    {
      "Disease": "Colonic Ulcer",
      "Laterality": "Cecum",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Not specified",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Colonic Ulcer>"
    },
    {
      "Disease": "Erythematous Mucosa",
      "Laterality": "Rectum",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Not specified",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Erythematous Mucosa>"
    },
    {
      "Disease": "Internal Hemorrhoids",
      "Laterality": "Not specified",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Not specified",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Internal Hemorrhoids>"
    },
    {
      "Disease": "LA Grade C Esophagitis",
      "Laterality": "Not specified",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Not specified",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for LA Grade C Esophagitis>"
    },
    {
      "Disease": "Gastroparesis",
      "Laterality": "Not specified",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Not specified",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Gastroparesis>"
    },
    {
      "Disease": "Gastritis",
      "Laterality": "Not specified",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Not specified",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Gastritis>"
    }
  ]
}
'''

sample_op='''{
      "Disease": "Dyspepsia",
      "Laterality": "Not specified",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Not specified",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Dyspepsia>"
    }'''

sample_op2 = '''{
  "Assessments": {"No Disease" : "0.00"}
}'''
#instruction = """Given the progress notes below, your task is to carefully identify and list all the diagnosis, paying attention to the specific details such as laterality, severity#, type, cause, and progression stage, that could influence to find the corresponding International Classification of Diseases (ICD) codes.
#Please exclude any conditions that the patient explicitly denies (e.g., phrases like 'denies,' 'negative for,' etc).
#Following the extraction process, compile the identified conditions in a list, prioritizing conditions of higher severity or urgency at the top, and present the data in a JSON##format in descending order based on their priority or severity.
#For example, below is the sample output:
#{
#  "Diseases": ["Fatty Liver","Leg Fracture"]
#}
#"""

instruction = """Pretend you as an expert medical coding specialist, the primary objective is to extract pertinent diseases from the provided progress notes for accurate ICD code assignment. Precision is of utmost importance, especially in the HPI, Subjective, and Assessment sections. The focus should be on identifying both acute and chronic conditions to ensure a comprehensive coding approach.
Guidelines:
Subjective Section:(CC,HPI, ROS, PFSH)
HPI (History of Present Illness):
Identify diseases mentioned in the chief complaints and any additional relevant details in the subjective assessment.
Extract specific diagnosis, signs and symptoms mentioned in the patient's recent medical history.
Pay close attention to any social history (smoking, unemployment ect) mentioned in the HPI.
Look for any chronic conditions that contribute to the patient's current health status
Objective Section (PE)
Abstract any conditions, signs and symptoms identified during the examination by the physician.
.
Assessment
Extract diseases explicitly diagnosed or assessed by the healthcare provider.
Plan
Review the treatment options. Extract relevan long term drugs.and current drug regime.
ICD Code Assignment:
Assign the diagnosis established after study which is chiefly responsible for the visits as the principal/first listed diagnosis followed by other evaluated conditions . Remove all the absracted sign and symptoms for teh respective diagnosis assined. If any specify treatment plan done for a specific sign or symtoms if can be coded.
Cross-verify the codes with the latest coding guidelines for precision.
Additional Considerations:
If a disease is mentioned without a corresponding ICD code, attempt to infer the most relevant code based on available information.
Seek clarification or additional details if necessary to ensure accurate coding.
Remember, the goal is to capture diseases exclusively, omitting extraneous information. Your meticulous attention to detail in disease identification and ICD code assignment is crucial for successful claim submissions

Please analyze the assessments from the provided output and present them in the following format:

Expected Sample Output Format:
{
  "Assessments": [{
"description":"Lung cancer",
    "code":"C34.90"},
    {
"description":"Allergic rhinitis",
    "code":"J30.1"
}]
}



Here is the medical note:

"""
formatted_output = '''
Please extract the Assessment from the below result

Expected Sample Output format:
{
  "Assessments": {"Dyspepsia":"K29.60",
  "History of esophageal ulcer": "K22.0"}
}


{
  "Assessments": [{
"description":"Lung cancer",
    "code":"C34.90"},
    {
"description":"Allergic rhinitis",
    "code":"J30.1"
}]
}

Below is the Result:
'''
app = Flask(__name__)


@app.route('/medical-entity', methods=['POST'])
def extract_medical_disease():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
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
    auth_token = request.headers.get('Authorization')
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    medical_notes = request.form.get('notes')
    if medical_notes is None:
        medical_notes = request.get_json().get('notes')
    medical_entity_result = ''
    diseases = ''
    #medical_notes = None
    if medical_notes is not None:
        t1 = datetime.now()
        message, results = api.get_response(instruction, medical_notes)
        t2 = datetime.now()
        print("Elapsed time for processing the prompt:",(t2-t1).total_seconds())
        # Parse the JSON string into a Python dictionary
        print('LLM Output')
        print(message)
        if '{' not in message:
            print('In Ifffffffffffff')
            message = sample_op2
        medical_entity_result = json.loads(message)
        diseases_list = medical_entity_result["Assessments"]
        diseases = diseases_list
        #diseases = medical_entity_result
    else:
        diseases_list = sample_op2
        diseases = diseases_list
    # Extract the 'Disease' field from each item in 'Diseases' and join them as a comma-separated string
    #diseases = ', '.join(disease['Disease'] for disease in medical_entity_result['Diseases'])
    api_response = {
        "Output": json.dumps(diseases, indent=2)
    }
    print(api_response)
    return api_response


@app.route('/')
def medical_entity_extraction_app():
    return 'Medical Entity Extraction!'

if __name__ == '__main__':
    print("---- Into the main Function ----")
    app.run(debug=True, host='0.0.0.0', port=5007)
