import scispacy
import spacy
# Core models
import en_core_sci_sm
import en_core_sci_md
import en_core_sci_lg
# NER specific models
import en_ner_bc5cdr_md
# Tools for extracting & displaying data
from spacy import displacy
import pandas as pd
import en_ner_bc5cdr_md

from entity_extraction_model import get_model

text1 = """This 23-year-old white female presents with complaint of allergies.  She used to have allergies when she 
lived in Seattle but she thinks they are worse here.  In the past, she has tried Claritin, and Zyrtec.  Both worked 
for short time but then seemed to lose effectiveness.  She has used Allegra also.  She used that last summer and she 
began using it again two weeks ago.  It does not appear to be working very well.  She has used over-the-counter 
sprays but no prescription nasal sprays.  She does have asthma but doest not require daily medication for this and 
does not think it is flaring up.,MEDICATIONS: , Her only medication currently is Ortho Tri-Cyclen and the Allegra.,
ALLERGIES: , She has no known medicine allergies.,OBJECTIVE:,Vitals:  Weight was 130 pounds and blood pressure 
124/78.,HEENT:  Her throat was mildly erythematous without exudate.  Nasal mucosa was erythematous and swollen.  Only 
clear drainage was seen.  TMs were clear.,Neck:  Supple without adenopathy.,Lungs:  Clear.,ASSESSMENT:,  
Allergic rhinitis.,PLAN:,1.  She will try Zyrtec instead of Allegra again.  Another option will be to use loratadine. 
 She does not think she has prescription coverage so that might be cheaper.,2.  Samples of Nasonex two sprays in each 
 nostril given for three weeks.  A prescription was written as well."""


def extract_entity(model, medical_note):
    nlp_bc = get_model(model)
    cleansed_note = ''
    if 'ROS:' in medical_note:
        parts1 = medical_note.split("ROS:")
        cleansed_note = cleansed_note + parts1[0]
        if 'Medical History:' in medical_note:
            parts2 = medical_note.split("Medical History:")
            cleansed_note = cleansed_note + "Medical History: "+parts2[1]
    else:
        cleansed_note = medical_note
    doc = nlp_bc(medical_note)
    entity_str = ""
    entities = doc.ents
    for ent in entities:
        entity_str = entity_str + ' ' + f'\n' + ent.text
    # displacy_image = displacy.render(doc, jupyter=True, style='ent')
    return entity_str


def extract_diseases(model, medical_notes):
    entity_str = extract_entity(model, medical_notes)
    disease_entities = ""
    # 9255184837977538312
    # 9255184837977538312
    nlp_bc5cdr = en_ner_bc5cdr_md.load()
    disease_sm = nlp_bc5cdr(entity_str)
    for entity in disease_sm.ents:
        if 9255184837977538312 == entity.label:
            disease_entities = disease_entities + ' ' + f'\n' + entity.text
    return disease_entities
