import os
import sys
import keyboard
from voxgravity.config import CONFIG
from voxgravity.audio import AudioRecorder
from voxgravity.bridge import FileBridge

def main():
    hotkey = CONFIG.get("hotkey", "shift+'")
    print("=" * 65)
    print("   🎙️ VOXGRAVITY - TERMINAL COMPANION (PUSH-TO-TOGGLE)")
    print(f"   1º toque [ {hotkey.upper()} ] : Começa a gravar (Beep agudo)")
    print(f"   2º toque [ {hotkey.upper()} ] : Para de gravar e envia (Beep médio)")
    print("   (Para encerrar o daemon: Ctrl + C no terminal)")
    print("=" * 65 + "\n")

    def on_start():
        print(f"\n🔴 [GRAVANDO...] Fale à vontade! Pressione [ {hotkey.upper()} ] novamente para encerrar.")

    def on_stop():
        print("⏳ [PAROU!] Transcrevendo sua fala...")

    def on_success(texto):
        print(f"✅ [Você disse]: \"{texto}\"")
        print("🚀 Enviado à Cristina via Bridge! Aguardando resposta...\n")

    def on_error(msg):
        print(f"⚠️ {msg}")

    recorder = AudioRecorder(
        on_start=on_start,
        on_stop=on_stop,
        on_success=on_success,
        on_error=on_error
    )

    try:
        keyboard.add_hotkey(hotkey, recorder.toggle)
        print(f"Pronto! Pressione [ {hotkey.upper()} ] em qualquer janela para falar.\n")
        keyboard.wait()
    except KeyboardInterrupt:
        print("\nEncerrando VoxGravity...")
    finally:
        recorder.fechar()
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass

if __name__ == "__main__":
    main()
