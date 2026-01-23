
from watsonAPI import Watson 

myWatson = Watson()


try:
    while(True):
        prompt = input("Pregúntame lo que quieras: ")
        if prompt == "salir":
            print("User finalized program. Bye")
            break
        print(prompt)
        response = myWatson.generate_text(prompt)
        print(response)
#print(json.dumps(response, indent=2))

except KeyboardInterrupt:
    print("User finalized program. Bye")
    