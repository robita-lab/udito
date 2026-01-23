from ComAct import ComAct

myCA = ComAct()
len = myCA.speak("Hola ¿cómo estás?", "HAPPY", 5)
print(len)


def main():
    print("Ejecutando ")

def interactive_test():

    print("TTS en tiempo real. Escribe 'salir' para terminar.")

    while True:
        text = input("Escribe el texto que quieres convertir en voz: ")
        if text.lower() == "salir":
            print("Saliendo del programa.")
            break
        elif text.lower() == "speaker":
            print("Speakers disponibles:")
            print(myCA.tts.coqui_speakers_idx)
            print(myCA.tts.watson_speakers_idx)
            speaker = input("Escribe el nombre del speaker: ")
            myCA.tts.set_tts_speaker(speaker)
        elif text.lower() == "calla":
            print("Shut UP - pause()")
            myCA.pause()
        else:
            try:
                len = myCA.speak(text, "YES", 5)
            except Exception as e:
                print(f"Error: {e}")

