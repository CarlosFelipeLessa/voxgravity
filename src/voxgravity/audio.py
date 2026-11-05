import os
import sys
import time
import winsound
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import pyperclip
from voxgravity.config import CONFIG
from voxgravity.bridge import FileBridge

class AudioRecorder:
    """Gerencia a captura contínua de microfone e transcrição via Push-to-Toggle."""
    
    def __init__(self, on_start=None, on_stop=None, on_success=None, on_error=None):
        self.esta_gravando = False
        self.stream = None
        self.audio_frames = []
        self.ultimo_clique = 0.0
        
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_success = on_success
        self.on_error = on_error
        
        audio_cfg = CONFIG.get("audio", {})
        self.sample_rate = audio_cfg.get("sample_rate", 16000)
        self.channels = audio_cfg.get("channels", 1)
        self.language = audio_cfg.get("language", "pt-BR")
        self.debounce = CONFIG.get("debounce_seconds", 0.35)
        
        beeps = CONFIG.get("beeps", {})
        self.beep_start = beeps.get("start_freq", 1200)
        self.beep_stop = beeps.get("stop_freq", 850)
        self.beep_sent = beeps.get("sent_freq", 1400)
        self.beep_error = beeps.get("error_freq", 450)

    def _audio_callback(self, indata, frames, time_info, status):
        if self.esta_gravando:
            self.audio_frames.append(indata.copy())

    def toggle(self) -> bool:
        """Alterna entre iniciar e parar a gravação com debounce."""
        agora = time.time()
        if agora - self.ultimo_clique < self.debounce:
            return self.esta_gravando
        self.ultimo_clique = agora

        if not self.esta_gravando:
            return self.iniciar_gravacao()
        else:
            return self.parar_e_transcrever()

    def iniciar_gravacao(self) -> bool:
        self.esta_gravando = True
        self.audio_frames = []
        
        try:
            winsound.Beep(self.beep_start, 150)
        except Exception:
            pass

        if self.on_start:
            self.on_start()

        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="int16",
                callback=self._audio_callback
            )
            self.stream.start()
            return True
        except Exception as e:
            self.esta_gravando = False
            if self.on_error:
                self.on_error(f"Erro no microfone: {e}")
            return False

    def parar_e_transcrever(self, auto_enviar: bool = True) -> bool:
        self.esta_gravando = False
        
        try:
            winsound.Beep(self.beep_stop, 150)
        except Exception:
            pass

        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
            self.stream = None

        if self.on_stop:
            self.on_stop()

        if not self.audio_frames:
            if self.on_error:
                self.on_error("Nenhum áudio gravado.")
            return False

        try:
            audio_data = np.concatenate(self.audio_frames, axis=0)
            audio_bytes = audio_data.tobytes()

            recognizer = sr.Recognizer()
            audio = sr.AudioData(audio_bytes, sample_rate=self.sample_rate, sample_width=2)
            texto = recognizer.recognize_google(audio, language=self.language)

            pyperclip.copy(texto)

            if auto_enviar:
                FileBridge.enviar_pergunta(texto)
                try:
                    winsound.Beep(self.beep_sent, 100)
                except Exception:
                    pass

            if self.on_success:
                self.on_success(texto)
            return True

        except sr.UnknownValueError:
            try:
                winsound.Beep(self.beep_error, 150)
            except Exception:
                pass
            if self.on_error:
                self.on_error("Não foi possível reconhecer a fala.")
            return False
        except Exception as e:
            try:
                winsound.Beep(400, 200)
            except Exception:
                pass
            if self.on_error:
                self.on_error(f"Erro: {e}")
            return False

    def fechar(self):
        self.esta_gravando = False
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
