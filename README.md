# 🎙️ VoxGravity

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)]()
[![Voice](https://img.shields.io/badge/TTS-Neural%20Edge-purple.svg)]()
[![IPC](https://img.shields.io/badge/IPC-FileBridge%20Zero--Focus-orange.svg)]()

**Zero-Latency Real-Time Voice Companion & File-Bridge IPC for AI Agents (Antigravity).**

[Visão Geral](#visão-geral) •
[Arquitetura](#arquitetura) •
[Funcionalidades](#funcionalidades) •
[Instalação Rápida](#instalação-rápida) •
[Como Usar](#como-usar) •
[Configuração](#configuração) •
[Segurança](#segurança)

</div>

---

## 📌 Visão Geral

O **VoxGravity** é um sistema completo de interação por voz bidirecional e ponte de comunicação entre o usuário e agentes de inteligência artificial (como Google Antigravity). 

Ele resolve o problema de roubo de foco de janela (*focus-stealing*) através de uma arquitetura limpa de **File-Bridge IPC**, combinada com captura contínua **Push-to-Toggle** (`Shift + '`) e reprodução neural de **latência zero** direto na memória.

---

## 🏗️ Arquitetura

```mermaid
flowchart TD
    subgraph Entrada de Voz
        U[Usuário] -->|Shift + '| A[Push-to-Toggle: Gravação Ativa]
        A -->|Shift + '| B[Parar & Transcrição SpeechRecognition]
        B -->|Áudio p/ Texto| C[bridge/pergunta.txt]
    end

    subgraph FileBridge IPC
        C -->|Monitor Passivo| D[Antigravity Agent]
        D -->|Raciocínio & Ferramentas| E[Resposta Gerada]
        E -->|Escrita| F[bridge/resposta.txt]
    end

    subgraph Saída de Voz (Zero-Latency)
        F -->|Detecção Automática| G[Edge-TTS Neural Synthesis]
        G -->|Stream em Memória| H[sounddevice.play - 0ms delay]
        H -->|Voz Cristina / Antonio| U
    end
```

---

## ✨ Funcionalidades Principais

- 🎙️ **Push-to-Toggle Inteligente**: Pressione `Shift + '` uma vez para começar a falar sem pressa; pressione novamente para encerrar e enviar. Sem cortes indesejados por silêncio.
- ⚡ **Reprodução com Latência Zero**: O áudio neural sintetizado é decodificado diretamente na memória via `soundfile` + `sounddevice`, eliminando gargalos de subprocessos externos.
- 🌉 **File-Bridge IPC Assíncrono**: Comunicação desacoplada entre a interface e o agente através de arquivos locais de fila (`bridge/pergunta.txt` e `bridge/resposta.txt`), garantindo que o agente nunca roube o foco de digitação da sua tela.
- 🎨 **Mini-Barra Flutuante (GUI)**: Interface moderna em Tkinter com suporte a arraste, auto-envio, botão de cópia rápida para clipboard e indicação visual de status.
- 💻 **Modo Terminal / Headless (CLI)**: Daemon leve em linha de comando que roda em segundo plano consumindo recursos mínimos de CPU e memória.
- 🎭 **Vozes Neurais Calibradas**:
  - `cristina`: Jovem, animada, espontânea e com dicção natural (tom +8Hz, velocidade +5%).
  - `antonio`: Masculino, encorpado, tranquilo e perfeito para sessões de trabalho (+0Hz / -8Hz).
  - `francisca`: Padrão formal neutro.
- 🔌 **Servidor MCP Integrado**: Compatível com o padrão Model Context Protocol (`mcp_server.py`), permitindo que agentes chamem as ferramentas de voz de forma nativa.

---

## 🚀 Instalação Rápida

### Pré-requisitos
- **Windows 10 / 11**
- **Python 3.10+** instalado e adicionado ao PATH do Windows.

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/CarlosFelipeLessa/voxgravity.git
cd voxgravity
```

### Passo 2: Executar o Instalador Automático
Dê dois cliques no arquivo:
```cmd
install.bat
```
O script cuidará de:
1. Criar o ambiente virtual isolado `.venv`
2. Atualizar o `pip`
3. Instalar todas as dependências do `requirements.txt`
4. Registrar o pacote no modo editável (`pip install -e .`)

---

## 🎯 Como Usar

### 1. Mini-Barra Flutuante (Recomendado)
Dê dois cliques em:
```cmd
iniciar_mini_barra.bat
```
- A barra ficará fixada no topo da tela (*always-on-top*).
- Pressione `Shift + '` em qualquer tela para ativar o microfone (beep agudo).
- Fale sua pergunta e pressione `Shift + '` novamente (beep médio).
- A pergunta é transcrita e enviada automaticamente via Bridge para o agente!

### 2. Modo Terminal (Daemon Headless)
Dê dois cliques em:
```cmd
iniciar_push_to_talk.bat
```
Executa diretamente pelo terminal para máxima economia de recursos.

### 3. Síntese Direta via Linha de Comando
```cmd
.venv\Scripts\python.exe falar_edge.py "Olá! Como posso te ajudar agora?" cristina
```

---

## ⚙️ Configuração

Você pode personalizar teclas de atalho, vozes e frequências de beeps diretamente em `config.json`:

```json
{
  "hotkey": "shift+'",
  "debounce_seconds": 0.35,
  "audio": {
    "sample_rate": 16000,
    "channels": 1,
    "language": "pt-BR"
  },
  "beeps": {
    "start_freq": 1200,
    "stop_freq": 850,
    "sent_freq": 1400,
    "error_freq": 450
  },
  "tts": {
    "default_voice": "cristina",
    "presets": {
      "cristina": {
        "voice": "pt-BR-ThalitaMultilingualNeural",
        "pitch": "+8Hz",
        "rate": "+5%"
      }
    }
  }
}
```

---

## 🔒 Segurança e Boas Práticas

- **Zero Exposição de Segredos**: O repositório utiliza um `.gitignore` rigoroso que bloqueia caches locais, arquivos `.env`, binários pesados de modelos e arquivos temporários de áudio.
- **Isolamento de Dados IPC**: As mensagens de áudio gravadas e transcritas na pasta `bridge/` são tratadas estritamente como efêmeras e nunca são comitadas no Git.
- **Caminhos Relativos**: Todo o código fonte resolve diretórios com base no pacote (`Path(__file__).resolve().parent...`), funcionando de forma idêntica em qualquer máquina sem dependência de caminhos absolutos hardcoded.

---

## 📁 Estrutura do Projeto

```
voxgravity/
├── .gitignore               # Regras de segurança e exclusão do Git
├── config.example.json      # Modelo de configurações
├── config.json              # Configurações ativas do usuário
├── install.bat              # Script de instalação de dependências e venv
├── iniciar_mini_barra.bat   # Launcher da Mini-Barra GUI
├── iniciar_push_to_talk.bat # Launcher do terminal CLI
├── LICENSE                  # Licença MIT
├── pyproject.toml           # Metadados do pacote Python
├── README.md                # Documentação completa
├── requirements.txt         # Dependências do projeto
├── mcp_server.py            # Servidor MCP de Voz
├── main.py                  # Ponto de entrada unificado
├── aguardar_pergunta.py     # Script bridge listener
├── mini_barra.py            # Atalho raiz para GUI
├── push_to_talk.py          # Atalho raiz para CLI
├── falar_edge.py            # Atalho raiz para TTS
└── src/
    └── voxgravity/
        ├── __init__.py      # Metadados do pacote
        ├── audio.py         # Gravação Push-to-Toggle e transcrição
        ├── bridge.py        # File-Bridge IPC
        ├── cli.py           # Daemon de terminal
        ├── config.py        # Carregador de configurações
        ├── tts.py           # Síntese neural e áudio in-memory
        └── ui.py            # Interface gráfica Tkinter
```

---

## 📄 Licença

Distribuído sob a licença **MIT**. Consulte [`LICENSE`](LICENSE) para mais detalhes.

---

<div align="center">
Desenvolvido com carinho para elevar a experiência de desenvolvimento e produtividade com agentes de IA.
</div>
