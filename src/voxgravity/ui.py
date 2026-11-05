import os
import sys
import time
import threading
import tkinter as tk
import keyboard
import pyperclip
from voxgravity.config import CONFIG, RESPOSTA_FILE
from voxgravity.bridge import FileBridge
from voxgravity.audio import AudioRecorder

class MiniBarraVoz:
    def __init__(self, root):
        self.root = root
        self.root.title("VoxGravity - Voice Bar")
        
        largura = 530
        altura = 140
        screen_w = self.root.winfo_screenwidth()
        pos_x = (screen_w - largura) // 2
        pos_y = 35
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#181825")
        
        self.auto_enviar = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Shift + ' para INICIAR e Shift + ' para PARAR")
        self.texto_var = tk.StringVar(value="")
        
        self.recorder = AudioRecorder(
            on_start=self._on_rec_start,
            on_stop=self._on_rec_stop,
            on_success=self._on_rec_success,
            on_error=self._on_rec_error
        )
        
        self._construir_interface()
        self._iniciar_atalho_global()
        self._iniciar_monitor_resposta()
        
    def _construir_interface(self):
        # 1. Barra de Título (Arrastável)
        self.header = tk.Frame(self.root, bg="#11111b", height=28)
        self.header.pack(fill=tk.X, side=tk.TOP)
        self.header.pack_propagate(False)
        
        self.header.bind("<ButtonPress-1>", self._iniciar_arraste)
        self.header.bind("<ButtonRelease-1>", self._parar_arraste)
        self.header.bind("<B1-Motion>", self._arrastar)
        
        lbl_titulo = tk.Label(
            self.header, 
            text="🎙️ VoxGravity Companion (Push-to-Toggle)", 
            fg="#cdd6f4", 
            bg="#11111b", 
            font=("Segoe UI", 9, "bold")
        )
        lbl_titulo.pack(side=tk.LEFT, padx=10)
        lbl_titulo.bind("<ButtonPress-1>", self._iniciar_arraste)
        lbl_titulo.bind("<B1-Motion>", self._arrastar)
        
        btn_fechar = tk.Button(
            self.header, 
            text="✕", 
            command=self.fechar, 
            fg="#f38ba8", 
            bg="#11111b", 
            activebackground="#f38ba8",
            activeforeground="#11111b",
            relief=tk.FLAT, 
            bd=0, 
            font=("Segoe UI", 9, "bold"),
            padx=8
        )
        btn_fechar.pack(side=tk.RIGHT)

        # 2. Corpo Principal
        corpo = tk.Frame(self.root, bg="#181825", padx=10, pady=6)
        corpo.pack(fill=tk.BOTH, expand=True)
        
        linha_topo = tk.Frame(corpo, bg="#181825")
        linha_topo.pack(fill=tk.X, pady=(0, 4))
        
        self.btn_mic = tk.Button(
            linha_topo,
            text="🎙️ Gravar (Shift + ')",
            command=self.toggle_gravacao,
            font=("Segoe UI", 9, "bold"),
            bg="#89b4fa",
            fg="#11111b",
            activebackground="#b4befe",
            activeforeground="#11111b",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2"
        )
        self.btn_mic.pack(side=tk.LEFT)
        
        self.lbl_status = tk.Label(
            linha_topo,
            textvariable=self.status_var,
            font=("Segoe UI", 8),
            fg="#a6adc8",
            bg="#181825",
            anchor="w"
        )
        self.lbl_status.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)

        # Campo do Texto Transcrito
        self.entry_texto = tk.Entry(
            corpo,
            textvariable=self.texto_var,
            font=("Segoe UI", 10),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief=tk.FLAT,
            bd=4
        )
        self.entry_texto.pack(fill=tk.X, pady=4)
        
        # Linha Inferior
        linha_baixo = tk.Frame(corpo, bg="#181825")
        linha_baixo.pack(fill=tk.X, pady=(2, 0))
        
        chk_auto = tk.Checkbutton(
            linha_baixo,
            text="Auto-enviar ao parar",
            variable=self.auto_enviar,
            font=("Segoe UI", 8),
            fg="#cdd6f4",
            bg="#181825",
            selectcolor="#313244",
            activebackground="#181825",
            activeforeground="#cdd6f4"
        )
        chk_auto.pack(side=tk.LEFT)
        
        btn_enviar = tk.Button(
            linha_baixo,
            text="🚀 Enviar Agora",
            command=self.enviar_para_antigravity,
            font=("Segoe UI", 8, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#94e2d5",
            activeforeground="#11111b",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=2,
            cursor="hand2"
        )
        btn_enviar.pack(side=tk.RIGHT, padx=(4, 0))

        btn_copiar = tk.Button(
            linha_baixo,
            text="📋 Copiar",
            command=self.copiar_texto,
            font=("Segoe UI", 8),
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            activeforeground="#cdd6f4",
            relief=tk.FLAT,
            bd=0,
            padx=6,
            pady=2,
            cursor="hand2"
        )
        btn_copiar.pack(side=tk.RIGHT)

    def _iniciar_arraste(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _parar_arraste(self, event):
        self._drag_x = None
        self._drag_y = None

    def _arrastar(self, event):
        if getattr(self, "_drag_x", None) is not None:
            dx = event.x - self._drag_x
            dy = event.y - self._drag_y
            novo_x = self.root.winfo_x() + dx
            novo_y = self.root.winfo_y() + dy
            self.root.geometry(f"+{novo_x}+{novo_y}")

    def _iniciar_atalho_global(self):
        def atalho_callback():
            self.root.after(0, self.toggle_gravacao)
        try:
            hotkey = CONFIG.get("hotkey", "shift+'")
            keyboard.add_hotkey(hotkey, atalho_callback)
        except Exception as e:
            print(f"[UI] Erro ao registrar atalho: {e}")

    def _iniciar_monitor_resposta(self):
        def monitor_loop():
            ultimo_mtime = 0
            while True:
                time.sleep(0.5)
                try:
                    if RESPOSTA_FILE.exists():
                        mtime = RESPOSTA_FILE.stat().st_mtime
                        if mtime > ultimo_mtime:
                            ultimo_mtime = mtime
                            with open(RESPOSTA_FILE, "r", encoding="utf-8") as f:
                                resp = f.read().strip()
                            if resp:
                                self.root.after(0, lambda r=resp: self._mostrar_resposta(r))
                except Exception:
                    pass
        threading.Thread(target=monitor_loop, daemon=True).start()

    def _mostrar_resposta(self, texto_resposta):
        self.status_var.set("💬 Resposta recebida do Agente!")
        self.texto_var.set(f"Cristina: {texto_resposta}")

    def toggle_gravacao(self):
        # Executa a alternância com thread separada na hora de transcrever
        if not self.recorder.esta_gravando:
            self.recorder.iniciar_gravacao()
        else:
            threading.Thread(target=lambda: self.recorder.parar_e_transcrever(auto_enviar=self.auto_enviar.get()), daemon=True).start()

    def _on_rec_start(self):
        self.root.after(0, lambda: self.btn_mic.configure(
            text="🔴 Parar (Shift + ')",
            bg="#f38ba8",
            fg="#11111b"
        ))
        self.root.after(0, lambda: self.status_var.set("Gravando... Pressione Shift + ' para encerrar!"))

    def _on_rec_stop(self):
        self.root.after(0, lambda: self.btn_mic.configure(
            text="⏳ Transcrevendo...",
            bg="#f9e2af",
            fg="#11111b"
        ))
        self.root.after(0, lambda: self.status_var.set("Processando sua fala..."))

    def _on_rec_success(self, texto):
        def _update():
            self.texto_var.set(texto)
            self.btn_mic.configure(text="🎙️ Gravar (Shift + ')", bg="#89b4fa", fg="#11111b")
            if self.auto_enviar.get():
                self.status_var.set("🚀 Enviado via Bridge! Processando...")
            else:
                self.status_var.set("✅ Transcrito! Clique em 'Enviar Agora'.")
        self.root.after(0, _update)

    def _on_rec_error(self, erro_msg):
        def _update():
            self.btn_mic.configure(text="🎙️ Gravar (Shift + ')", bg="#89b4fa", fg="#11111b")
            self.status_var.set(f"⚠️ {erro_msg}")
        self.root.after(0, _update)

    def copiar_texto(self):
        texto = self.texto_var.get().strip()
        if texto:
            pyperclip.copy(texto)
            self.status_var.set("📋 Copiado para a área de transferência!")

    def enviar_para_antigravity(self):
        texto = self.texto_var.get().strip()
        if not texto:
            self.status_var.set("⚠️ Fale ou digite algo primeiro!")
            return
        if FileBridge.enviar_pergunta(texto):
            self.status_var.set("🚀 Enviado à Cristina! Ela já está processando...")
        else:
            self.status_var.set("Erro ao gravar no arquivo de bridge.")

    def fechar(self):
        self.recorder.fechar()
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MiniBarraVoz(root)
    root.protocol("WM_DELETE_WINDOW", app.fechar)
    root.mainloop()

if __name__ == "__main__":
    main()
