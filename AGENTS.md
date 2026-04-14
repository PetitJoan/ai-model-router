# 🤖 AGENTS.md — Reglas del Router para RooCode

## 🧠 Capacidades del Sistema (v2.0)
Este proyecto utiliza un **AI Model Router** con contexto dinámico bidireccional. 

### Reglas para los Agentes:
1.  **Contexto Masivo (Hasta 128k):** No temas realizar tareas que requieran mucha memoria o archivos largos. El router ampliará automáticamente el contexto si es necesario.
2.  **Uso de Visión (MCP):** Si estás trabajando en CSS o Web, puedes solicitar capturas de pantalla a través del MCP. El router gestionará el aumento de tokens automáticamente.
3.  **Gestión de Pausas:** El router puede reiniciar el servidor al expandir el contexto (~15s). Si recibes un error de red momentáneo, espera unos segundos y reintenta; el servidor está arrancando.
4.  **Optimización de Velocidad:** Si la tarea es pequeña, el router reducirá el contexto a 64k para ganar velocidad. No necesitas hacer nada; es automático.

### Perfiles de Modelo:
- `architect`: Razonamiento profundo (Thinking ON).
- `orchestrator`: Planificación y coordinación (Thinking ON).
- `code`: Desarrollo y edición (Thinking ON).
- `ask`: Preguntas rápidas y depuración (Thinking OFF).

## 💡 Consejos para el Agente:
- Si el usuario reporta lentitud extrema, sugiere un "Reset Context" para forzar al router a hacer un **Auto-Shrink** al tamaño base.
- Si una tarea de visión falla por timeout, reduce el número de imágenes en el historial.
