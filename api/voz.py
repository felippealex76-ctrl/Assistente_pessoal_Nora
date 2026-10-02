import pyttsx3

def criar_voz():
    engine = pyttsx3.init()
    engine.setProperty("rate",180)

    for voz in engine.getProperty("voices"):
        nome = voz.name.lower()
        if"portug" in nome or "brazil" in nome or "maria" in nome or "daniel" in nome:
            engine.setProperty("voice", voz.id)
            break
    
    return engine

def falar(texto):
    engine = criar_voz()
    engine.say(texto)
    engine.runAndWait()

if __name__=="__main__":
    falar("Olá! Eu sou a Nora, sua assistente pessoal. ")
    "Prazer em finalmente falar com você!"