#
# Interfaz de conexión con el sistema watson assistant de IBM
#
#
# pip install ibm-watsonx-ai
#

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods

import json

class Watson():    
    def __init__(self, result_callback = None):      
        print("Watson::ctor")
        url = "https://eu-de.ml.cloud.ibm.com"        
#        api_key = "TP8qCL22zUpXkw2mHMtoAwJJZqM9ZBzKSwV_kPR60E0S"  # la de tu servicio watsonx.ai
        api_key = "W4Lj_7EVx2wnLJU-rAMWVbpFltJfT3k-HtbeA-FnCD_l"  # la de tu servicio watsonx.ai
        self.project_id = "adc42d4e-54a7-450d-893a-09e07d3c90df"  # el ID del proyecto watsonx que creaste
        region = "eu-de"
        model_id = "ibm/granite-4-h-small"
        #    model_id = client.foundation_models.TextModels.FLAN_T5_XXL,
        #    model_id="ibm/granite-3-8b-instruct",
        #    model_id="meta-llama/llama-3-3-70b-instruct",

        #    GenParams().get_example_values()

        self.credentials = Credentials(
                   url = url,
                   api_key = api_key
                  )

        self.gen_parms = {
            GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
            GenParams.MAX_NEW_TOKENS: 100,
            GenParams.STOP_SEQUENCES: ["\n"] #"stop_sequences": ["\n\n"],
        }

        self.model = ModelInference(
            model_id = model_id,
            params = self.gen_parms,
            credentials = self.credentials,
            project_id = self.project_id
        )

        self.header = "<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a helpful assistant. Keep your answers short and to the point. Do not cut sentences. Answer always in Spanish.<|eot_id|><|start_header_id|>user<|end_header_id|>"
        self.footer = "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

    def change_model(self, model_id):
        self.model = ModelInference(
            model_id = model_id,
            params = self.gen_parms,
            credentials = self.credentials,
            project_id = self.project_id
        )

    def generate_text(self, text):
        prompt = self.header + text + self.footer
        try:
            response = self.model.generate_text(
                prompt = prompt,
                params = self.gen_parms
            )
            return response
        except:
            print("Watson::no_response")
            return None
