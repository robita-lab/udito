#
# pip install ibm-watsonx-ai
#

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods

import json


#<|begin_of_text|><|header_start|>system<|header_end|>
#
#SYSTEM PROMPT<|eot|><|header_start|>user<|header_end|>
#
#USER_INPUT<|eot|><|header_start|>assistant<|header_end|>


url = "https://eu-de.ml.cloud.ibm.com"
api_key = "TP8qCL22zUpXkw2mHMtoAwJJZqM9ZBzKSwV_kPR60E0S"  # la de tu servicio watsonx.ai
project_id = "b65c1eaa-91ac-4520-9a79-ce25df3876a0"  # el ID del proyecto watsonx que creaste
region = "eu-de"
model_id = "ibm/granite-4-h-small"
#    model_id = client.foundation_models.TextModels.FLAN_T5_XXL,
#    model_id="ibm/granite-3-8b-instruct",
#    model_id="meta-llama/llama-3-3-70b-instruct",

credentials = Credentials(
                   url = url,
                   api_key = api_key
                  )

#client = APIClient(credentials)
GenParams().get_example_values()

gen_parms = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MAX_NEW_TOKENS: 100,
    GenParams.STOP_SEQUENCES: ["\n"] #"stop_sequences": ["\n\n"],
}

model = ModelInference(
    model_id = model_id,
    params = gen_parms,
    credentials=credentials,
    project_id=project_id
)

# === Prompt y generación ===
#prompt = "Explícame la diferencia entre inteligencia artificial débil y fuerte."
#prompt = "resumen en dos frases cómo funciona la fotosíntesis?"
prompt = "Explícame la diferencia entre inteligencia artificial débil y fuerte"

header = "<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a helpful assistant. Keep your answers short and to the point. Do not cut sentences.<|eot_id|><|start_header_id|>user<|end_header_id|>"
footer = "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

try:
    while(True):
        text = input("Pregúntame lo que quieras: ")
        if text == "salir":
            print("User finalized program. Bye")
            break
        prompt= header + text + footer
        print(prompt)
        response = model.generate_text(
            prompt=prompt, 
            params= gen_parms
            )
        print(response)
#print(json.dumps(response, indent=2))

except KeyboardInterrupt:
    print("User finalized program. Bye")