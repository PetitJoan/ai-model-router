# Contribuyendo a AI Model Router

Bienvenido! Queremos que contribuyas a este proyecto. Esta guía te ayudará a entender cómo puedes contribuir de manera efectiva.

## 📋 Tabla de Contenidos

- [Código de Conducta](#-código-de-conducta)
- [Cómo Contribuir](#-cómo-contribuir)
- [Flujo de Trabajo](#-flujo-de-trabajo)
- [Estilos de Código](#-estilos-de-código)
- [Guía de Estilo para Commits](#-guía-de-estilo-para-commits)
- [Desarrollo](#-desarrollo)
- [Pruebas](#-pruebas)
- [Estructura del Proyecto](#-estructura-del-proyecto)

## 📜 Código de Conducta

Nuestro código de conducta está definido en [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Por favor, léelo antes de contribuir.

## 🎯 Cómo Contribuir

### Tipos de Contribuciones

1. **Bugs**: Reportar problemas encontrados
2. **Features**: Añadir nuevas funcionalidades
3. **Documentación**: Mejorar la documentación existente
4. **Traducciones**: Traducir la documentación a otros idiomas
5. **Optimizaciones**: Mejorar el rendimiento
6. **Refactorización**: Mejorar el código sin cambiar funcionalidad

### Reportando Bugs

Antes de reportar un bug:

1. Asegúrate de que no es un problema conocido (revisa los issues abiertos)
2. Proporciona información detallada:
   - Versión del software
   - Sistema operativo
   - Pasos para reproducir el problema
   - Expected behavior vs actual behavior
   - Capturas de pantalla si es relevante

**Ejemplo de reporte de bug:**

```markdown
**Título:** [Bug] El router no cambia de modelo cuando se usa enable_thinking

**Descripción:**
Al cambiar de un perfil con enable_thinking:true a uno con enable_thinking:false, el router no libera correctamente la VRAM.

**Pasos para reproducir:**
1. Iniciar router con perfil "architect" (enable_thinking: true)
2. Cambiar a perfil "ask" (enable_thinking: false)
3. Verificar uso de VRAM

**Expected:** VRAM liberada
**Actual:** VRAM sigue ocupada

**Entorno:**
- OS: Windows 11
- Python: 3.10
- llama.cpp: 2024.01.01
```

### Sugerencias de Features

Para sugerir nuevas características:

1. Explica el problema que resuelve
2. Describe la solución propuesta
3. Proporciona ejemplos de uso
4. Menciona alternativas consideradas

## 🔄 Flujo de Trabajo

### 1. Clona el Repositorio

```bash
git clone https://github.com/tu-usuario/ai_model_router.git
cd ai_model_router
```

### 2. Crea una Rama

```bash
# Para bugs
git checkout -b fix/nombre-del-bug

# Para nuevas features
git checkout -b feature/nombre-de-la-feature
```

### 3. Haz tus Cambios

Sigue las guías de estilo y pruebas.

### 4. Prueba tus Cambios

```bash
python AI_MODEL_ROUTER.py
```

### 5. Haz Commit

```bash
git add .
git commit -m "feat: añade nueva funcionalidad de X"
```

### 6. Envía Pull Request

1. Ve al repositorio en GitHub
2. Haz clic en "Compare & pull request"
3. Revisa tus cambios
4. Envía la PR

## 💻 Estilos de Código

### Python Style Guide

Este proyecto sigue las convenciones de [PEP 8](https://pep8.org/):

- **Indentación**: 4 espacios
- **Líneas máximas**: 88 caracteres
- **Espacios en blanco**: Siguiendo PEP 8
- **Comentarios**: Claros y explicativos

### Ejemplo de Código

```python
"""AI Model Router - Proxy inteligente para RooCode.

Este módulo gestiona dinámicamente múltiples modelos de IA en llama.cpp.
"""

import asyncio
import json
import logging
from typing import Dict, Optional, List
from aiohttp import web

logger = logging.getLogger(__name__)


class ModelRouter:
    """Clase principal para enrutar peticiones a modelos específicos."""

    def __init__(self, config_path: str = "config.json"):
        """Inicializa el router con la configuración especificada.

        Args:
            config_path: Ruta al archivo de configuración JSON.
        """
        self.config = self._load_config(config_path)
        self.active_model: Optional[str] = None
        self.processes: Dict[str, asyncio.Process] = {}

    def _load_config(self, config_path: str) -> Dict:
        """Carga la configuración desde un archivo JSON.

        Args:
            config_path: Ruta al archivo de configuración.

        Returns:
            Diccionario con la configuración cargada.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Archivo de configuración no encontrado: {config_path}")
            raise

    async def start_model(self, model_name: str) -> None:
        """Inicia un modelo específico.

        Args:
            model_name: Nombre del perfil de modelo a iniciar.
        """
        if model_name not in self.config.get("profiles", {}):
            raise ValueError(f"Perfil de modelo no encontrado: {model_name}")

        # Implementación del inicio del modelo
        pass
```

## 📝 Guía de Estilo para Commits

Usa el formato [Conventional Commits](https://www.conventionalcommits.org/):

### Tipos de Commits

| Tipo | Prefijo | Descripción |
|------|---------|-------------|
| Feature | `feat:` | Nueva funcionalidad |
| Fix | `fix:` | Corrección de bug |
| Docs | `docs:` | Cambios en documentación |
| Style | `style:` | Formateo de código (sin cambios lógicos) |
| Refactor | `refactor:` | Refactorización de código |
| Perf | `perf:` | Mejoras de rendimiento |
| Test | `test:` | Añadir o actualizar pruebas |
| Chore | `chore:` | Tareas de mantenimiento |

### Ejemplos de Commits

```bash
# Nueva feature
git commit -m "feat: añade soporte para múltiples instancias de backend"

# Corrección de bug
git commit -m "fix: corrige error en la liberación de VRAM al cambiar de modelo"

# Documentación
git commit -m "docs: actualiza README.md con nuevos endpoints"

# Refactorización
git commit -m "refactor: simplifica la lógica de enrutamiento de peticiones"

# Pruebas
git commit -m "test: añade pruebas para la gestión de procesos"
```

## 🛠️ Desarrollo

### Entorno de Desarrollo

Recomendamos usar un entorno virtual:

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Desarrollo con VS Code

Recomendamos las siguientes extensiones:

- Python
- Pylance
- Black Formatter
- Flake8

### Configuración de Debug

Crea un archivo `.vscode/launch.json` para debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: AI Model Router",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/AI_MODEL_ROUTER.py",
            "console": "integratedTerminal",
            "python": "${workspaceFolder}/venv/bin/python"
        }
    ]
}
```

## 🧪 Pruebas

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas específicas
pytest tests/test_router.py

# Ejecutar con cobertura
pytest --cov=AI_MODEL_ROUTER.py --cov-report=html
```

### Escribir Pruebas

Usamos [pytest](https://docs.pytest.org/):

```python
"""Pruebas para el router de modelos."""

import pytest
from AI_MODEL_ROUTER import ModelRouter


class TestModelRouter:
    """Pruebas para la clase ModelRouter."""

    @pytest.fixture
    def router(self, tmp_path):
        """Crea un router de prueba."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"profiles": {"test": {"args": []}}}')
        return ModelRouter(str(config_file))

    def test_load_config(self, router):
        """Prueba que la configuración se carga correctamente."""
        assert router.config is not None

    @pytest.mark.asyncio
    async def test_start_model(self, router):
        """Prueba el inicio de un modelo."""
        await router.start_model("test")
        assert router.active_model == "test"
```

### Cobertura de Pruebas

Mantener una cobertura mínima del 80%:

```bash
# Ver cobertura
pytest --cov=AI_MODEL_ROUTER.py

# Cobertura en HTML
pytest --cov=AI_MODEL_ROUTER.py --cov-report=html -cov-report=term-missing
```

## 📁 Estructura del Proyecto

```
ai_model_router/
├── AI_MODEL_ROUTER.py      # Script principal
├── config.json             # Configuración
├── requirements.txt        # Dependencias
├── tests/                  # Pruebas
│   ├── __init__.py
│   ├── test_router.py
│   └── test_config.py
├── docs/                   # Documentación
│   ├── api.md
│   └── architecture.md
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── .gitignore
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

## 📊 Checklist para Pull Requests

Antes de enviar un Pull Request, verifica:

- [ ] El código sigue las guías de estilo
- [ ] Las pruebas pasan (`pytest`)
- [ ] La cobertura de pruebas no disminuye
- [ ] La documentación está actualizada
- [ ] Los commits siguen el formato Conventional Commits
- [ ] No hay commits irrelevantes
- [ ] Se han añadido pruebas para nuevas funcionalidades
- [ ] Se han actualizado los mensajes de error si es necesario

## 🙏 Agradecimientos

Gracias por contribuir! Tu trabajo ayuda a mejorar este proyecto para toda la comunidad.

---

**¡Gracias por contribuir!** 🎉
