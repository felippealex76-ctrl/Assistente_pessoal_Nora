import asyncio
import os
import re
import tempfile
import uuid

import numpy as np
import sounddevice as sd
import edge_tts
from playsound import playsound

VOZ = "pt-BR-FranciscaNeural"
TAXA = 16000
LIMIAR_VOZ = 600   # sensibilidade da interrupção por voz (maior = precisa falar mais alto)


async def _gerar_audio(texto, caminho):
    comunicacao = edge_tts.Communicate(texto, VOZ)
    await comunicacao.save(caminho)


def falar(texto):
    """Gera a fala (voz neural) e toca até o fim. Para confirmações curtas."""
    texto = (texto or "").strip()
    if not texto:
        return
    print(f"[VOZ] falando: {texto}")
    nome = f"nora_{uuid.uuid4().hex}.mp3"
    caminho = os.path.join(tempfile.gettempdir(), nome)
    asyncio.run(_gerar_audio(texto, caminho))
    playsound(caminho)
    try:
        os.remove(caminho)
    except OSError:
        pass


def _ouviu_voz(dur=0.25):
    """Escuta um instante e diz se há voz (nível acima do limiar)."""
    try:
        bloco = sd.rec(int(dur * TAXA), samplerate=TAXA, channels=1, dtype="int16")
        sd.wait()
        nivel = float(np.abs(bloco).mean())
        return nivel > LIMIAR_VOZ
    except Exception:
        return False


def falar_interrompivel(texto):
    """Fala frase por frase; se ouvir voz no respiro entre frases, para.
    Retorna True se foi interrompida. Sem eco, pois checa o microfone em silêncio."""
    frases = [f for f in re.split(r'(?<=[.!?])\s+', (texto or "").strip()) if f]
    for frase in frases:
        falar(frase)
        if _ouviu_voz():
            return True
    return False


if __name__ == "__main__":
    print(falar_interrompivel("Esta é uma explicação longa. Pode me interromper falando que eu paro na hora."))
