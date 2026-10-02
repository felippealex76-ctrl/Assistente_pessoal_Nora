import asyncio
import os
import tempfile

import edge_tts
from playsound import playsound

# Voz feminina brasileira. Veja outras com:  edge-tts --list-voices
VOZ = "pt-BR-FranciscaNeural"


async def _gerar_audio(texto, caminho):
    comunicacao = edge_tts.Communicate(texto, VOZ)
    await comunicacao.save(caminho)


def falar(texto):
    caminho = os.path.join(tempfile.gettempdir(), "nora_fala.mp3")
    asyncio.run(_gerar_audio(texto, caminho))
    playsound(caminho)


if __name__ == "__main__":
    falar("Olá! Agora eu falo com uma voz de verdade. Bem melhor, né?")