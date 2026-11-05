import asyncio
import os
import sys
from pathlib import Path
import edge_tts
import sounddevice as sd
import soundfile as sf
from voxgravity.config import CONFIG, ROOT_DIR

TEMP_AUDIO_PATH = ROOT_DIR / "ultima_fala_edge.mp3"

async def synthesize_async(text: str, voice_cfg: dict, output_file: Path) -> None:
    """Sintetiza texto em áudio MP3 de alta fidelidade usando edge-tts."""
    comm = edge_tts.Communicate(
        text,
        voice_cfg["voice"],
        pitch=voice_cfg.get("pitch", "+0Hz"),
        rate=voice_cfg.get("rate", "+0%")
    )
    await comm.save(str(output_file))

def play_audio(audio_file: Path, block: bool = True) -> None:
    """Reproduz áudio diretamente na memória sem dependência de processos do PowerShell."""
    try:
        data, fs = sf.read(str(audio_file))
        sd.play(data, fs)
        if block:
            sd.wait()
    except Exception as e:
        print(f"[TTS] Erro ao reproduzir áudio: {e}")

def falar(texto: str, voz: str = None, block: bool = True) -> bool:
    """Sintetiza e reproduz em voz alta com o preset configurado."""
    texto = texto.strip()
    if not texto:
        return False
    
    tts_config = CONFIG.get("tts", {})
    voz_escolhida = (voz or tts_config.get("default_voice", "cristina")).lower()
    presets = tts_config.get("presets", {})
    
    cfg = presets.get(voz_escolhida, presets.get("cristina", {
        "voice": "pt-BR-ThalitaMultilingualNeural",
        "pitch": "+8Hz",
        "rate": "+5%"
    }))
    
    try:
        asyncio.run(synthesize_async(texto, cfg, TEMP_AUDIO_PATH))
        play_audio(TEMP_AUDIO_PATH, block=block)
        return True
    except Exception as e:
        print(f"[TTS] Falha na síntese de voz: {e}")
        return False

if __name__ == "__main__":
    texto = sys.argv[1] if len(sys.argv) > 1 else "Olá! Sistema de voz VoxGravity operacional."
    voz = sys.argv[2] if len(sys.argv) > 2 else "cristina"
    falar(texto, voz=voz)
