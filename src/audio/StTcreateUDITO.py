#
# creates a language model and add the word UDITO
#
# ibm_cloud_sdk_core.api_exception.ApiException: Error: This feature is not available for the Bluemix Lite plan. Please upgrade to a paid plan to activate this feature: https://console.bluemix.net/catalog/services/speech-to-text, Status code: 400 , X-global-transaction-id: 46258a39-379b-423f-af86-d7c6f4e5988f 
#
#  curl -X POST -u "apikey:GcPMqCjN5je8m_Ef62KZNEm2xjnuyWaIEBtGuN-bFdvk" --header "Content-Type: application/json" --data "{\"name\": \"es_ES-UDITO\",   \"base_model_name\": \"es-ES_Multimedia\",   \"description\": \"Example custom language model\"}" "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/customizations"


from StT import StT

def my_function( result ):
    print(f"result: :{result}")

myStT = StT(my_function)
print("Creando un nuevo modelo custom y añade UDITO")
myStT.create_custom_model()
language_models = myStT.list_custom_models()
print(json.dumps(language_models, indent=2))

print("Entrenando modelo")
myStS.train_custom_model(language_models)

print("Subiendo modelo")
myStS.upgrade_custom_model(language_models)

input("Pulse una tecla para comenzar...")
myStS.start()
input("Pulse una tecla para finalizar...")
myStT.close()


