from StT import StT

def result_callback( result ):
    print(f"result: :{result}")

def user_callback( flag ):
    print(f"user_speaking: {flag}")

myStT = StT(result_callback, user_callback)
myStT.start()
input("Pulse una tecla para finalizar...")
myStT.close()


