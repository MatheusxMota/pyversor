# Notas de Desenvolvimento e Pendências

Este arquivo contém o histórico de melhorias técnicas e observações sobre o projeto.

## Changelog

### [14/07/2026] - Migração para Pipeline 100% Local
*   **Descrição:** Substituição da geração de vídeo via API Hugging Face (SVD) por um pipeline local e gratuito.
*   **Mudanças:**
    *   Implementado `KenBurnsMotionProvider` para animação local (zoom/pan) usando `moviepy`.
    *   Implementado sistema de mixagem de áudio (narração + trilha de fundo com controle de volume e fade-out).
    *   Criada estrutura `musicas/` para gerenciamento de trilhas sonoras.
    *   Endpoint `/identificar-e-gerar-video/` agora opera 100% sem chamadas de rede para vídeo.
    *   Removida dependência obrigatória de API externa para a etapa de vídeo.

### [14/07/2026] - Atualização para moviepy v2.2.1
*   **Descrição:** Correção de incompatibilidades de API introduzidas pelo `moviepy` 2.x.
*   **Mudanças:**
    *   Atualizada sintaxe em `services/video_service.py` para usar `vfx` e `afx` (`Loop`, `AudioFadeOut`).
    *   Adicionado sistema de gerenciamento de fontes em `assets/fonts/` com fallback automático de segurança caso a fonte não seja encontrada.
    *   Limpeza de código morto e imports desnecessários.

## Relatório de Análise Técnica (Atualizado em 14/07/2026)

Aqui está o status atual dos pontos identificados:

### 1. Problemas de Performance (Sincronismo no Async)
*   **Status: Resolvido.**
*   **Descrição**: O método `generate_video` em `services/image_to_video_service.py` foi refatorado para utilizar `httpx.AsyncClient`, eliminando o bloqueio do *event loop* do FastAPI.

### 2. Gerenciamento de Arquivos e "Smells" de Código
*   **Status: Parcialmente Resolvido.**
*   **Descrição**: A gestão de manipuladores de arquivos em `services/video_service.py` foi melhorada com o uso de blocos `try...finally` e chamadas explícitas de `.close()`.
*   **Pendência**: O `time.sleep(0.5)` ainda é utilizado como *workaround* para liberar arquivos temporários no Windows. Recomenda-se investigar alternativas mais robustas ou garantir que o `moviepy` libere os handles corretamente sem necessidade de espera artificial.

### 3. Boas Práticas
*   **Status: Resolvido.**
*   **Descrição**: A chamada `load_dotenv()` foi centralizada no ponto de entrada da aplicação (`app.py`), eliminando redundâncias nos módulos de serviço.

---

### Conclusão
O código está significativamente mais organizado e performático. As prioridades imediatas foram endereçadas. A única pendência residual é a melhoria na robustez da limpeza de arquivos temporários, substituindo o `time.sleep` por um mecanismo de liberação mais preciso.
