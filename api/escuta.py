import sounddevice as sd
import speech_recognition as sr

TAXA = 16000
DURACAO = 5

def ouvir(duracao=DURACAO):
    print(" ouvindo... pode falar.")
    gravacao = sd.rec(int(duracao * TAXA), samplerate=TAXA, channels=1, dtype="int16")
    sd.wait()

    audio = sr.AudioData(gravacao.tobytes(), TAXA, 2)

    reconhecedor = sr.Recognizer()
    try:
        texto = reconhecedor.recognize_google(audio, language="pt-BR")
        print("você disse:", texto)
        return texto
    except sr.UnknownValueError:
        print("não consegui entender o que vocÊ falou.")
        return ""
    except sr.RequestError:
        print("Erro ao acessar o serviço de reconhecimento ( sem internet?).")
        return ""
if __name__== "__main__":
    ouvir()

