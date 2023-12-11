import en_core_sci_sm
import en_core_sci_md
import en_core_sci_lg

import en_ner_bc5cdr_md


# ner_bc5
# ner_bionlp
# core_sci_sm
# core_sci_md
# core_sci_lg

def get_model(model_type):
    match model_type:
        # case 'ner_bc5':
        #     return en_ner_bc5cdr_md.load()
        # case 'ner_bionlp':
        #     return en_ner_bionlp13cg_md.load()
        case 'core_sci_sm':
            return en_core_sci_sm.load()
        case 'core_sci_md':
            return en_core_sci_md.load()
        case 'core_sci_lg':
            return en_core_sci_lg.load()
