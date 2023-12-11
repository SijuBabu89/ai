from insuranceLLM import api

import time
import gradio as gr


instruction = """Given the progress notes below, your task is to carefully identify and list all the diagnosis, paying attention to the specific details such as laterality, severity, type, cause, and progression stage, that could influence to find the corresponding International Classification of Diseases (ICD) codes.
Please exclude any conditions that the patient explicitly denies (e.g., phrases like 'denies,' 'negative for,' etc).
Following the extraction process, compile the identified conditions in a list, prioritizing conditions of higher severity or urgency at the top, and present the data in a JSON format in descending order based on their priority or severity.
For example, below is the sample output:
{
  "Diseases": [
    {
      "Disease": "Fatty Liver",
      "Laterality": "Not specified",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Alcholic",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Fattly Liver>"
    },
    {
      "Disease": "Leg Fracture",
      "Laterality": "Right",
      "Severity": "Not specified",
      "Type": "Not specified",
      "Cause": "Accident",
      "Progression Stage": "Not specified",
      "ICD" : "<ICD for Leg Fracture>
     }
  ]
}
"""

def slow_echo(query, history, instruction=instruction):
    message, results = api.get_response(instruction, query)
    for i in range(len(message)):
        time.sleep(0.1)
        yield message[:i+1]

gr.ChatInterface(slow_echo, theme="soft").queue().launch(share=True)
