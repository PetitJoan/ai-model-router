# 🚀 AI Model Router para RooCode + llama.cpp (v2.0)

**AI Model Router** es un proxy inteligente escrito en Python que actúa como intermediario optimizado entre la extensión **RooCode** y el servidor local **llama.cpp**. 

Diseñado específicamente para gestionar modelos potentes (Qwen 27B/35B) en máquinas con recursos de VRAM finitos, permitiendo una experiencia fluida y con una memoria masiva.

---

## 🌟 Características Principales (v2.0)

### 1. 🧠 Gestión de Contexto Dinámico Bidireccional
El router analiza cada petición de Roo Code y ajusta el servidor en tiempo real:
*   **Auto-Expansión:** Si la conversación crece, el router reinicia el servidor ampliando la ventana de contexto (hasta 128k). ¡Se acabaron los errores de "context size exceeded"!
*   **Auto-Shrink (Reducción):** Si limpias el chat o empiezas una tarea pequeña, el router reduce el contexto al valor base (64k). Esto libera VRAM y hace que el modelo responda mucho más rápido.

### 2. 👁️ Soporte Inteligente para Visión (MCP)
Optimizado para trabajar con herramientas de captura de pantalla (MCP) y CSS:
*   Detecta automáticamente imágenes en la petición.
*   Suma un margen de seguridad de tokens para evitar colapsos al procesar capturas de pantalla de sitios web.

### 3. ⚡ Arquitectura Anti-Bloqueo
Implementa un sistema de colas asíncronas que evita que Roo Code se quede "colgado" mientras el modelo se carga en la VRAM. Las peticiones esperan pacientemente su turno sin romper la conexión.

---

## 🛠️ Requisitos e Instalación

### Requisitos
*   **Python 3.10+**
*   **llama.cpp** (con `llama-server.exe`) instalado en `C:\Llama.cpp` (o la ruta que configures).
*   **Dependencias:** `aiohttp` (el router la instalará automáticamente si no la tienes).

### Instalación Rápida
1. Descarga o clona este repositorio.
2. Asegúrate de tener tus modelos `.gguf` en la carpeta de llama.cpp.
3. Ejecuta el router:
   ```powershell
   python AI_MODEL_ROUTER.py
   ```
   *(O usa el archivo `.bat` incluido)*.

---

## ⚙️ Configuración en Roo Code

Para conectar Roo Code con el Router, usa estos parámetros:

1.  **Provider:** `OpenAI Compatible`
2.  **Base URL:** `http://localhost:8080`
3.  **API Key:** `any` (no se requiere, pero el campo no puede estar vacío)
4.  **Model ID:** Elige uno de estos perfiles:
    *   `architect`: Máximo razonamiento (Qwen 27B Thinking).
    *   `orchestrator`: Planificación compleja (Qwen 35B Thinking).
    *   `code`: Edición de archivos (Qwen 27B Thinking).
    *   `ask`: Consultas rápidas y depuración (Qwen 27B No-Thinking).
    *   `default`: Respuesta instantánea (Qwen 9B).

---

## 📊 Panel de Control (CMD)

El router proporciona información en tiempo real en tu consola:
*   **`--> architect (~45000 tokens)`**: Indica que Roo Code ha enviado una petición de ese tamaño.
*   **`⚠ REINICIO DINAMICO`**: Aviso visual de que el contexto está cambiando para adaptarse a la tarea.
*   **`✓ Listo en 12.5s`**: Confirmación de que el modelo está cargado y listo para responder.

---

## 💡 Consejos de Uso Profesional
*   **Limpieza de Contexto:** Si notas que el modelo se vuelve lento tras una tarea de visión muy pesada (128k), simplemente limpia el chat en Roo Code. El router detectará la reducción y volverá a los 64k base para recuperar velocidad.
*   **VRAM vs RAM:** Con 16GB de VRAM, el router intentará mantener lo máximo posible en la GPU. El resto se desbordará a tu RAM (128GB), garantizando que el sistema nunca falle por falta de memoria.

---
*Desarrollado para ofrecer la máxima libertad y potencia en el desarrollo de software con IA local.*
