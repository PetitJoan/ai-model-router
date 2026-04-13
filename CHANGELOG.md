# Changelog

Todos los cambios importantes en este proyecto se documentarán en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.0.0/), y este proyecto sigue [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-04-12

### ✨ Primer Lanzamiento

#### Características Principales

- **Proxy inteligente para RooCode**: Intermediario entre RooCode y llama.cpp
- **Gestión dinámica de modelos**: Cambia entre modelos según el modo de RooCode
- **Múltiples perfiles de modelo**: Soporte para Architect, Code, Ask, Debug y Default
- **API compatible con OpenAI**: Compatible con la API de OpenAI para fácil integración
- **Monitorización en tiempo real**: Endpoint para verificar el estado del router
- **Gestión limpia de procesos**: Cierra servidores de forma segura al detener el router

#### Modelos Soportados

- **Architect**: Modelos de razonamiento profundo (27B/35B) con `enable_thinking: true`
- **Code**: Modelos de razonamiento profundo para generación de código
- **Ask**: Modelos rápidos para preguntas sin razonamiento profundo
- **Debug**: Modelos optimizados para depuración
- **Default**: Modelos ligeros de 9B como fallback

#### Configuración

- Archivo `config.json` para configuración de modelos
- Soporte para múltiples perfiles con diferentes parámetros
- Mapeo de aliases para nombres de modelos

#### Documentación

- README.md con instrucciones completas
- LEEME.md con documentación en español
- LICENSE con licencia MIT
- INICIAR-AI_MODEL_ROUTER.bat para inicio en Windows

---

## [0.2.0] - Próximamente

### 🚀 Mejoras Planificadas

- Soporte para múltiples instancias de backend
- Métricas y estadísticas detalladas
- Interfaz web de administración
- Soporte para modelos adicionales (vLLM, Ollama)
- Sistema de caché para respuestas frecuentes

---

## [0.1.0] - 2026-04-12

### 🐛 Correcciones

- (Ninguna en el lanzamiento inicial)

### 📝 Documentación

- (Ninguna en el lanzamiento inicial)

---

## [0.0.1] - 2026-04-12

### 🧪 Desarrollo

- Estructura inicial del proyecto
- Implementación básica del router
- Configuración inicial de modelos

---

# Guía de Versiones

## Formato de Versión

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Cambios incompatibles hacia atrás
- **MINOR**: Nuevas funcionalidades hacia atrás compatibles
- **PATCH**: Correcciones de bugs hacia atrás compatibles

## Tipos de Cambios

| Sección | Descripción |
|---------|-------------|
| `Added` | Nuevas características |
| `Changed` | Cambios existentes |
| `Deprecated` | Características que serán eliminadas |
| `Removed` | Características eliminadas |
| `Fixed` | Correcciones de bugs |
| `Security` | Correcciones de seguridad |

## Ejemplo de Entrada

```markdown
## [1.0.0] - 2024-01-01

### Added
- Nueva función de X
- Soporte para Y

### Changed
- Cambiado Z de A a B

### Fixed
- Corregido error en C
```

---

## Historial de Versiones

### Versión Actual: 0.1.0

**Fecha de lanzamiento**: 12 de abril de 2026

**Estado**: Estable

**Notas**:
- Primer lanzamiento estable
- Compatible con Python 3.8+
- Requiere llama.cpp instalado

---

## Notas sobre el Proyecto

### Dependencias Clave

- **Python**: >= 3.8
- **aiohttp**: >= 3.9.0
- **llama.cpp**: Cualquier versión compatible

### Sistemas Operativos Soportados

- Windows 10/11
- Linux (Ubuntu, Debian, Fedora, etc.)
- macOS

### Hardware Recomendado

- **VRAM**: Mínimo 8GB para modelos de 9B, 16GB+ para modelos de 27B/35B
- **CPU**: Multi-core recomendado
- **RAM**: 16GB+ recomendado

---

## Contribuidores

Gracias a todos los contribuidores que han ayudado a hacer este proyecto mejor.

---

## Reportar Bugs

Si encuentras un bug o tienes una sugerencia de mejora, por favor abre un [issue](https://github.com/tu-usuario/ai_model_router/issues).

---

**Última actualización**: 12 de abril de 2026
