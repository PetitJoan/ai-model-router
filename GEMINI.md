# GEMINI.md - Contexto de Instrucciones para AI Model Router

## 🚀 Resumen del Proyecto
**AI Model Router** es un proxy inteligente en Python que optimiza la conexión entre **RooCode** y **llama.cpp**, permitiendo gestionar modelos grandes (27B/35B) con recursos finitos.

### 🎯 Gestión de Contexto Bidireccional (v2.0)
El router implementa un sistema de **Auto-Ajuste de Contexto**:
1.  **Expansión Dinámica:** Si la petición supera el contexto actual, reinicia el servidor ampliándolo (bloques de 8k) hasta el `global_max_context` (128k por defecto).
2.  **Auto-Shrink (Reducción):** Si la petición es pequeña (<80% del contexto base), reinicia el servidor para volver al tamaño base (64k). Esto libera VRAM y recupera velocidad de respuesta.
3.  **Soporte Vision (MCP):** Detecta imágenes en el payload y suma automáticamente 3.000 tokens por imagen a la estimación.

## 🏗️ Arquitectura y Componentes
- **`AI_MODEL_ROUTER.py`**:
  - `estimate_tokens_from_payload()`: Heurística avanzada (2.5 chars/token + 3k por imagen).
  - `switch_profile()`: Gestión de ciclo de vida con `boot_event` para evitar bloqueos en el router.
- **Endpoints**:
  - `/_router/status`: Información sobre perfil activo, contexto real y estado de carga.

## 💡 Notas para el Agente
- **Prioridad de VRAM:** El router está optimizado para 16GB de VRAM. Mantén el `-ngl` alto pero vigila el uso de KV Cache en contextos de 128k.
- **Tiempos de Carga:** El cambio de contexto tarda ~15s. No interrumpas el proceso; el router gestiona las esperas automáticamente.
- **Consola:** Los avisos de reinicio dinámico son críticos para que el usuario sepa por qué hay una pausa en la respuesta.
