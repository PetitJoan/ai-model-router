# AI Model Router

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

**Proxy inteligente para RooCode que gestiona dinámicamente múltiples modelos de IA en llama.cpp**

[English (README.md)](./README.md)

</div>

## 🎯 ¿Qué es AI Model Router?

**AI Model Router** es un proxy HTTP ligero escrito en Python que actúa como intermediario entre la extensión de desarrollo **RooCode** y tu servidor local de IA **llama.cpp**.

### El Problema que Resuelve

RooCode tiene diferentes "modos" de trabajo (Architect, Code, Ask, Debug, etc.). Lo ideal es usar un modelo de razonamiento profundo y pesado (ej. 27B/35B) para tareas de arquitectura y código, pero un modelo más ligero y rápido (ej. 9B) para preguntas rápidas o depuración.

Si tienes una PC doméstica, **no puedes cargar todos esos modelos en la VRAM de tu tarjeta gráfica al mismo tiempo.**

**AI Model Router soluciona esto:**

1. Escucha las peticiones de RooCode.
2. Identifica qué "modo" se está utilizando.
3. Si el modelo necesario no está cargado, **detiene el servidor actual de llama.cpp (liberando la VRAM)**.
4. **Arranca inmediatamente un nuevo servidor** con el modelo y la configuración específica requerida.
5. Espera a que el nuevo modelo cargue y redirige la petición sin que RooCode pierda la conexión.

## ✨ Características Principales

- 🔄 **Cambio Dinámico de Modelos**: Cambia entre modelos según el modo de RooCode sin reiniciar manualmente.
- 🛡️ **Validación Proactiva de Rutas**: Comprueba automáticamente si los archivos `.gguf` y el ejecutable de `llama-server` existen antes de intentar el cambio, evitando estados de error.
- 📊 **Observabilidad en Tiempo Real**: Endpoint dedicado `/_router/metrics` para rastrear tiempos de carga, uso de perfiles y tasas de error.
- 🚀 **Auto-detección**: Búsqueda inteligente de `llama-server.exe` en tu directorio base.
- 🔧 **Configuración Flexible**: Define múltiples perfiles de modelos con parámetros personalizados (thinking mode, flash attention, etc.).
- 🌐 **API Compatible con OpenAI**: Funciona perfectamente con cualquier cliente que espere una API estilo OpenAI.

## 📋 Requisitos Previos

- **Python 3.8** o superior.
- **[llama.cpp](https://github.com/ggerganov/llama.cpp)** instalado en tu equipo.
- Modelos de IA en formato `.gguf` descargados localmente.
- `aiohttp` (se instalará automáticamente en el primer arranque).

## ⚙️ Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/ai-model-router.git
cd ai-model-router
```

### 2. Configurar

Copia el archivo de configuración de ejemplo:

```bash
cp config.example.json config.json
```

Edita `config.json` para que coincida con tus rutas locales:
- Ajusta `base_dir` a tu carpeta de llama.cpp.
- Actualiza las rutas de los modelos en la sección de `profiles`.

### 3. Ejecutar el Router

**Windows:**
```bash
INICIAR-AI_MODEL_ROUTER.bat
```

**Terminal:**
```bash
python AI_MODEL_ROUTER.py
```

## 🛠️ Configuración (`config.json`)

| Campo | Descripción |
|-------|-------------|
| `base_dir` | Ruta principal donde tienes instalado `llama.cpp`. |
| `llama_exe_path` | Ruta al ejecutable `llama-server` (puede ser relativa a `base_dir`). |
| `router_port` | Puerto donde RooCode se conectará (por defecto: `8080`). |
| `startup_timeout` | Segundos máximos para esperar a que un modelo cargue (defecto: `120`). |
| `profiles` | Definición de perfiles de modelo disponibles y sus argumentos para `llama-server`. |

### Resolución Inteligente de Rutas
El router resuelve automáticamente las rutas relativas en los argumentos de tus perfiles. Si una ruta termina en `.gguf` o sigue a `-m`/`--model`, se buscará dentro de tu `base_dir`.

## 🌍 Ecosistema y Recursos

Este proyecto forma parte de un potente stack de desarrollo con IA local. Estos son los componentes principales:

*   **[RooCode](https://github.com/RooCodeAI/RooCode)**: Un asistente de programación avanzado para VS Code que soporta múltiples modos especializados (Architect, Code, etc.).
*   **[llama.cpp](https://github.com/ggerganov/llama.cpp)**: La implementación en C++ estándar de la industria para inferencia de LLMs de alto rendimiento.
*   **[Modelos GGUF en Hugging Face](https://huggingface.co/models?search=gguf)**: El mejor lugar para encontrar modelos pre-cuantizados listos para usar con este router.

## 🛠️ Profundizando en la Configuración Avanzada

Las configuraciones de ejemplo en este proyecto no son arbitrarias. Están optimizadas para hardware moderno (probado en 16GB+ de VRAM):

### Explicación de los Flags de Optimización Clave:

| Flag | Propósito | ¿Por qué usarlo? |
|------|-----------|-----------------|
| `-ngl 99` | Offloading a GPU | Fuerza todas las capas del modelo a la VRAM para máxima velocidad. |
| `--flash-attn` | Flash Attention | Reduce significativamente el uso de memoria y acelera el procesamiento en contextos largos. |
| `--cache-type-k q4_0` | Cuantización de Caché KV | Reduce el consumo de VRAM de la ventana de contexto, permitiendo modelos más grandes o chats más largos. |
| `--chat-template-kwargs '{"enable_thinking":true}'` | Modo Razonamiento | Específico para modelos Qwen/DeepSeek para habilitar el proceso de "pensamiento" durante la generación. |

## 💡 Buenas Prácticas y Consejos de Optimización

Para sacar el máximo provecho de tus LLMs locales, sigue estas recomendaciones probadas por la comunidad:

### 1. El "Punto Dulce" de la Cuantización
No utilices modelos de 16-bit o incluso 8-bit a menos que tengas muchísima VRAM. Para la mayoría de los casos:
*   **Q4_K_M**: El estándar de oro. Pérdida de inteligencia mínima (~0.1-0.2% de perplejidad) para una reducción de tamaño del 50%.
*   **Q5_K_M / Q6_K**: Úsalos para modelos de razonamiento (modo Architect) si tienes VRAM de sobra.
*   **Evita Q2/Q3**: Estos modelos tienen muchas más "alucinaciones", especialmente en tareas de programación.

### 2. Recomendaciones según tu Hardware

| VRAM | Modelo Recomendado | `-ngl` Sugerido | Contexto (`-c`) |
|------|--------------------|-----------------|-----------------|
| **8 GB** | 7B - 9B (Q4_K_M) | 40 - 60 | 8k - 16k |
| **12 GB** | 12B - 14B (Q4_0) | 60 - 80 | 16k - 24k |
| **16 GB** | 27B (Q3_K_M/Q4_0) | 99 (Máximo) | 32k |
| **24 GB+** | 35B+ (Q4_K_M) | 99 (Máximo) | 32k - 64k |

### 3. Sincronización de Contexto con RooCode
Si configuras `-c 32768` en tu `config.json`, establece en RooCode una **Ventana de Contexto (Context Window)** de unos **30,000**. Este margen de seguridad evita errores de desbordamiento (Context Overflow) que pueden colgar la inferencia o hacer que el modelo olvide el inicio de la conversación.

### 4. Monitoreo de VRAM
Mientras el router cambia de modelo, vigila el uso de tu VRAM:
*   **Windows**: Administrador de Tareas -> Rendimiento -> GPU -> Memoria dedicada de la GPU.
*   **Linux/Windows**: Ejecuta `nvidia-smi -l 1` en una terminal aparte para ver la asignación en tiempo real.

## 🎓 Aprende Más: Modelos Personalizados y Cuantización

Si quieres ir más allá de los modelos pre-fabricados y crear tus propias versiones optimizadas:

1.  **Conversión de Modelos**: Aprende a usar `convert_hf_to_gguf.py` en el [directorio de scripts de llama.cpp](https://github.com/ggerganov/llama.cpp/tree/master/convert_hf_to_gguf.py).
2.  **Guía de Cuantización**: Consulta la [documentación de cuantización de llama.cpp](https://github.com/ggerganov/llama.cpp#quantization) para entender el equilibrio entre tamaño del modelo (Q4, Q8, etc.) e inteligencia.
3.  **Formato GGUF**: Lee sobre la [especificación GGUF](https://github.com/ggerganov/llama.cpp/blob/master/docs/gguf.md) para entender por qué es el formato más eficiente para LLMs locales.

## 📊 Monitorización y Métricas

El router proporciona dos endpoints internos principales:

- **Estado**: `http://localhost:8080/_router/status` - Perfil activo actual y PID del proceso.
- **Métricas**: `http://localhost:8080/_router/metrics` - Estadísticas detalladas:
  - **Uptime**: Cuánto tiempo lleva el router encendido.
  - **Uso de Perfiles**: Contador de peticiones por perfil.
  - **Tiempos de Carga**: Duración de la última carga y tiempo medio por modelo.
  - **Registro de Errores**: Contador de tiempos de espera (timeouts) y errores de proxy.

## 🔌 Configuración Paso a Paso en Roo Code

Para que Roo Code se comunique correctamente con el Router y aproveche el cambio dinámico de modelos, sigue estos pasos:

### 1. Abrir la Configuración de Roo Code
Haz clic en el icono del **engranaje (Settings)** en la parte inferior de la extensión Roo Code en VS Code.

### 2. Configurar el Proveedor
En la sección de ajustes, localiza y configura los siguientes campos:

- **Provider**: Selecciona `OpenAI Compatible`.
- **Base URL**: Introduce `http://localhost:8080/v1` (asegúrate de incluir el `/v1`).
- **API Key**: Puedes introducir cualquier texto (ej. `local-router`). El router no la valida, pero Roo Code la requiere.
- **Model ID**: Introduce el nombre del perfil que deseas usar. **Debe coincidir exactamente** con uno de los `model_aliases` definidos en tu `config.json`.
    - *Ejemplos comunes:* `qwen3.5-orchestrator`, `qwen3.5-architect`, `qwen3.5-code`.

### 3. Ajustar la Ventana de Contexto
- **Max Context Window**: Debe coincidir (o ser ligeramente inferior) al parámetro `-c` definido en tus perfiles de `config.json`. 
    - *Recomendación:* Si en el router tienes `-c 32768`, pon `30000` en Roo Code para dejar un margen de seguridad.

### 4. Uso de Perfiles de Configuración (Recomendado)
Roo Code permite guardar **Settings Profiles**. Te recomendamos crear uno para cada tarea principal:

1.  Configura Roo Code para el modo **Architect** (usando el ID `qwen3.5-architect`).
2.  Haz clic en el selector de perfiles de Roo Code (arriba de los ajustes) y selecciona **"Save as new profile..."**.
3.  Ponle un nombre como `Roo-Architect`.
4.  Repite el proceso para `Roo-Code` (usando el ID `qwen3.5-code`).

**¿Cómo funciona el cambio dinámico?**
Cuando cambias de perfil en Roo Code o simplemente cambias el "Model ID" en los ajustes, el Router detectará el cambio en la siguiente petición. Si el modelo solicitado es distinto al que está cargado actualmente, el Router detendrá el servidor anterior y cargará el nuevo automáticamente. **Verás un breve retraso en la respuesta inicial mientras el modelo se carga en la VRAM.**

---

## 📝 Licencia

Este proyecto está bajo la licencia [MIT License](LICENSE).

---
**Hecho con ❤️ para la comunidad de desarrollo con IA.**
