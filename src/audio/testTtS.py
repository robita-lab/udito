from TtS import TtS
# Esto es una primera frase. Luego viene una segunda. Una tercera, y así. 
def robot_speaking_callback(flag):
    print(f"Robot Speaking: {flag}")

myTtS = TtS(robot_speaking_callback)
myTtS.speak("Hola,cómo estás?")
myTtS.tick()
#myTtS.tts_to_file_watson("Inicializando sistema...")

print("TTS en tiempo real. Escribe 'salir' para terminar.")

while True:
    text = input("Escribe el texto que quieres convertir en voz: ")
    if text.lower() == "salir":
        print("Saliendo del programa.")
        myTtS.close()
        break
    elif text.lower() == "speaker":
        print("Speakers disponibles:")
        print(myTtS.coqui_speakers_idx)
        print(myTtS.watson_speakers_idx)
        speaker = input("Escribe el nombre del speaker: ")
        myTtS.set_tts_speaker(speaker)
    elif text.lower() == "calla":
        print("Shut UP - pause()")
        myTtS.pause()
    else:
        try:
        # Generar audio como numpy array
        # myTtS.speak_es(text)
            myTtS.speak(text)
            myTtS.activate()
            print("utt leng: %" %(len(myTtS.ad)))
        except Exception as e:
            print(f"Error: {e}")
