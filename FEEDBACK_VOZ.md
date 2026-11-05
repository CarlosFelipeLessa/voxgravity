# Diretrizes de Resposta e Feedback por Voz (VoxGravity / Antigravity)

Sempre que o usuário solicitar uma tarefa prática, demorada ou que envolva pesquisas e modificações de arquivos, o agente/copiloto DEVE seguir estritamente este ciclo de comunicação de 3 etapas:

---

### 1. Aviso Imediato de Início (Ack Instantâneo)
- Assim que receber uma requisição de ação (modificar arquivo, rodar testes, varrer processos, instalar pacotes, etc.), o agente **deve imediatamente enviar e falar uma mensagem curta de confirmação**.
- **Objetivo:** Informar ao usuário que a requisição foi recebida e que a execução já começou, evitando silêncio enquanto processa.
- **Exemplo de fala:** *"Iniciando a modificação no arquivo agora mesmo!"* ou *"Certo, iniciando a varredura agora!"*.

---

### 2. Atualização Contínua de Etapas (Sem Silêncio Longo)
- Em tarefas que tenham múltiplas etapas ou que demorem mais de alguns segundos, forneça avisos curtos de progresso.
- **Objetivo:** Manter o usuário ciente do andamento e garantir que o copiloto não pareça travado.
- **Exemplo de fala:** *"Localizei o caminho, aplicando as alterações agora..."*.

---

### 3. Resumo Final de Conclusão
- Ao concluir toda a tarefa, forneça o resumo completo e claro das alterações ou resultados obtidos, tanto em texto quanto pelo canal de áudio.
- Re-arme a escuta em segundo plano para a próxima interação do usuário.
