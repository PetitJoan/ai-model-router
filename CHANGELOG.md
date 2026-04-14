# 📜 CHANGELOG — AI Model Router

## [v2.0] - 2026-04-14
### 🚀 Novedades Críticas
- **Contexto Bidireccional:** El router ahora no solo amplía el contexto, sino que lo **reduce (Auto-Shrink)** si la conversación se acorta. Esto libera memoria GPU y acelera drásticamente las respuestas cortas.
- **Soporte Vision (MCP):** Implementada la estimación inteligente de tokens para imágenes (3.000 tokens/img). Ideal para trabajar con CSS y capturas de pantalla de webs.
- **Arquitectura No Bloqueante:** Introducido `asyncio.Event` (`boot_event`). El router ya no se queda "colgado" durante el arranque del backend; las peticiones esperan ordenadamente.
- **Contexto Base 64k:** Aumentado el valor por defecto en todos los perfiles a 65.536 tokens para evitar reinicios innecesarios en tareas medianas.

### 🛠️ Mejoras
- **Heurística de Tokens:** Ajustada a 2.5 caracteres por token + 1.000 tokens de margen para prevenir errores 400 de `llama-server`.
- **Nueva Interfaz de Consola:** Panel informativo al inicio con instrucciones de configuración para Roo Code y validación de perfiles.
- **Auto-detección mejorada:** Mejor soporte para rutas absolutas y relativas del ejecutable `llama-server.exe`.

### 🐞 Correcciones
- Solucionado el problema de "hang" (bloqueo) de Roo Code cuando el servidor tardaba más de 30s en cargar un modelo de 35B.
- Corregida la subestimación de tokens en payloads con mensajes de sistema largos.
