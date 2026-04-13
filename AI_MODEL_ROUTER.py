"""
AI_MODEL_ROUTER.py  —  Router inteligente para RooCode + llama.cpp
================================================================
Escucha en :8080 y redirige cada peticion al servidor llama.cpp
correcto segun el modelo solicitado por RooCode.

Cuando cambia de modelo, para el servidor activo y arranca el nuevo.
El cambio tarda ~10-30 segundos (carga del modelo en VRAM).

Uso:
    python AI_MODEL_ROUTER.py
"""

import asyncio
import json
import logging
import re
import subprocess
import sys
import time
from pathlib import Path

# ─────────────────────────────────────────────────────────────
#  VERIFICACION E INSTALACION DE DEPENDENCIAS
# ─────────────────────────────────────────────────────────────
def check_dependencies():
    try:
        import aiohttp
    except ImportError:
        print("La libreria 'aiohttp' no esta instalada.")
        print("Instalando dependencias automaticamente...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
            print("Dependencias instaladas correctamente. Reiniciando importacion...\n")
        except subprocess.CalledProcessError:
            print("Error: No se pudo instalar 'aiohttp'. Por favor, instalala manualmente con: pip install aiohttp")
            sys.exit(1)

check_dependencies()

import aiohttp
from aiohttp import web

# ─────────────────────────────────────────────────────────────
#  CONFIGURACION POR DEFECTO
# ─────────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "base_dir": "C:\\Llama.cpp",
    "llama_exe_path": "",  # Vacío activa auto-detección por defecto
    "router_port": 8080,
    "backend_port": 8099,
    "startup_timeout": 120,
    "profiles": {
        "architect": {
            "description": "27B Thinking — Architect",
            "args": [
                "-m", "gguf/Qwen3.5-27B/Qwen3.5-27B-UD-Q3_K_XL.gguf",
                "--mmproj", "gguf/Qwen3.5-27B/mmproj-F16.gguf",
                "-c", "32768",
                "-ngl", "99",
                "--cache-type-k", "q4_0",
                "--cache-type-v", "q4_0",
                "--flash-attn", "on",
                "-t", "20", "-tb", "20",
                "--no-mmap", "--jinja",
                "--chat-template-kwargs", '{"enable_thinking":true}',
                "--temp", "0.6",
                "--top-p", "0.95",
                "--top-k", "20",
                "--min-p", "0.0",
                "--repeat-penalty", "1.0",
                "--presence-penalty", "0.0",
                "--threads-http", "4"
            ]
        },
        "orchestrator": {
            "description": "35B-A3B Thinking — Orchestrator",
            "args": [
                "-m", "gguf/Qwen3.5-35B/Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf",
                "--mmproj", "gguf/Qwen3.5-35B/mmproj-F16.gguf",
                "-c", "32768",
                "-ngl", "99",
                "--cache-type-k", "q4_0",
                "--cache-type-v", "q4_0",
                "--flash-attn", "on",
                "-t", "20", "-tb", "20",
                "--no-mmap", "--jinja",
                "--chat-template-kwargs", '{"enable_thinking":true}',
                "--temp", "1.0",
                "--top-p", "0.95",
                "--top-k", "20",
                "--min-p", "0.0",
                "--repeat-penalty", "1.0",
                "--presence-penalty", "1.5",
                "--threads-http", "4"
            ]
        },
        "code": {
            "description": "27B Thinking — Code",
            "args": [
                "-m", "gguf/Qwen3.5-27B/Qwen3.5-27B-UD-Q3_K_XL.gguf",
                "--mmproj", "gguf/Qwen3.5-27B/mmproj-F16.gguf",
                "-c", "32768",
                "-ngl", "99",
                "--cache-type-k", "q4_0",
                "--cache-type-v", "q4_0",
                "--flash-attn", "on",
                "-t", "20", "-tb", "20",
                "--no-mmap", "--jinja",
                "--chat-template-kwargs", '{"enable_thinking":true}',
                "--temp", "0.6",
                "--top-p", "0.95",
                "--top-k", "20",
                "--min-p", "0.0",
                "--repeat-penalty", "1.0",
                "--presence-penalty", "0.0",
                "--threads-http", "4"
            ]
        },
        "ask": {
            "description": "27B No-Think — Ask/Debug",
            "args": [
                "-m", "gguf/Qwen3.5-27B/Qwen3.5-27B-UD-Q3_K_XL.gguf",
                "--mmproj", "gguf/Qwen3.5-27B/mmproj-F16.gguf",
                "-c", "32768",
                "-ngl", "99",
                "--cache-type-k", "q4_0",
                "--cache-type-v", "q4_0",
                "--flash-attn", "on",
                "-t", "20", "-tb", "20",
                "--no-mmap", "--jinja",
                "--chat-template-kwargs", '{"enable_thinking":false}',
                "--temp", "0.7",
                "--top-p", "0.8",
                "--top-k", "20",
                "--min-p", "0.0",
                "--repeat-penalty", "1.0",
                "--presence-penalty", "1.5",
                "--threads-http", "4"
            ]
        },
        "debug": {
            "description": "27B No-Think — Ask/Debug",
            "args": [
                "-m", "gguf/Qwen3.5-27B/Qwen3.5-27B-UD-Q3_K_XL.gguf",
                "--mmproj", "gguf/Qwen3.5-27B/mmproj-F16.gguf",
                "-c", "32768",
                "-ngl", "99",
                "--cache-type-k", "q4_0",
                "--cache-type-v", "q4_0",
                "--flash-attn", "on",
                "-t", "20", "-tb", "20",
                "--no-mmap", "--jinja",
                "--chat-template-kwargs", '{"enable_thinking":false}',
                "--temp", "0.7",
                "--top-p", "0.8",
                "--top-k", "20",
                "--min-p", "0.0",
                "--repeat-penalty", "1.0",
                "--presence-penalty", "1.5",
                "--threads-http", "4"
            ]
        },
        "default": {
            "description": "9B No-Think — fallback rapido",
            "args": [
                "-m", "gguf/Qwen3.5-9B/Qwen3.5-9B-UD-Q4_K_XL.gguf",
                "--mmproj", "gguf/Qwen3.5-9B/mmproj-F16.gguf",
                "-c", "32768",
                "-ngl", "99",
                "--cache-type-k", "bf16",
                "--cache-type-v", "bf16",
                "--flash-attn", "on",
                "-t", "20", "-tb", "20",
                "--no-mmap", "--jinja",
                "--chat-template-kwargs", '{"enable_thinking":false}',
                "--temp", "0.7",
                "--top-p", "0.8",
                "--top-k", "20",
                "--min-p", "0.0",
                "--repeat-penalty", "1.0",
                "--presence-penalty", "1.5",
                "--threads-http", "4"
            ]
        }
    },
    "model_aliases": {
        "qwen3.5-orchestrator": "orchestrator",
        "orchestrator":         "orchestrator",
        "qwen3.5-architect":   "architect",
        "qwen3.5-code":        "code",
        "qwen3.5-ask":         "ask",
        "qwen3.5-debug":       "debug",
        "architect":           "architect",
        "code":                "code",
        "ask":                 "ask",
        "debug":               "debug"
    }
}

# ─────────────────────────────────────────────────────────────
#  ESTADO GLOBAL Y LOGGING
# ─────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("router")

CONFIG_FILE = Path(__file__).parent / "config.json"

def load_config():
    if not CONFIG_FILE.exists():
        log.info(f"No se encontro {CONFIG_FILE.name}. Creando archivo de configuracion por defecto...")
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
            log.info(f"Archivo de configuracion creado exitosamente.")
        except Exception as e:
            log.error(f"Error al crear el archivo de configuracion: {e}")
            sys.exit(1)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # ✅ AUTO-DETECT: Si llama_exe_path está vacío o no existe, buscar automáticamente
        if not config.get("llama_exe_path"):
            log.info("Detectando automáticamente la ruta de llama-server.exe...")
            try:
                # Crear BASE_DIR temporalmente para la búsqueda
                temp_base_dir = Path(config["base_dir"])
                config["llama_exe_path"] = find_llama_exe(temp_base_dir)
                log.info(f"✓ Ruta detectada exitosamente: {config['llama_exe_path']}")
            except FileNotFoundError as e:
                log.error(f"✗ No se pudo detectar automáticamente: {e}")
                log.error("Por favor, configura manualmente 'llama_exe_path' en config.json.")
                sys.exit(1)
        
        return config
    except json.JSONDecodeError as e:
        log.error(f"Error al leer config.json. Comprueba que el formato JSON sea correcto. Detalles: {e}")
        sys.exit(1)
    except Exception as e:
        log.error(f"Error inesperado al leer config.json: {e}")
        sys.exit(1)


def find_llama_exe(base_dir: Path) -> str:
    """
    Busca llama-server.exe con múltiples estrategias de búsqueda.
    
    Estrategias (en orden de prioridad):
    1. Buscar en carpetas que coincidan con patrón llama-\d+\.\d+-bin-win-.*
    2. Búsqueda recursiva con rglob
    
    Args:
        base_dir: Directorio base donde buscar (debe ser Path)
    
    Returns:
        Ruta absoluta de llama-server.exe encontrado
    
    Raises:
        FileNotFoundError: Si no se encuentra el ejecutable
    """
    exe_name = "llama-server.exe"
    
    # Estrategia A: Buscar en carpetas de versiones (llama-*.bin-win-*)
    for item in sorted(base_dir.iterdir()):
        if item.is_dir():
            # Verificar si coincide con patrón de versión de llama.cpp
            if re.match(r"llama-\d+\.\d+-bin-win-.*", item.name):
                exe_path = item / exe_name
                if exe_path.exists():
                    return str(exe_path.resolve())
    
    # Estrategia B: Buscar recursivamente todo el árbol
    for path in base_dir.rglob(exe_name):
        return str(path.resolve())
    
    raise FileNotFoundError(
        f"No se encontró llama-server.exe en {base_dir}. "
        f"Verifica que la instalación de llama.cpp existe correctamente."
    )


# ─────────────────────────────────────────────────────────────
#  VALIDACION DE RUTAS
# ─────────────────────────────────────────────────────────────
def validate_profile_paths(profile_key: str, profile: dict, base_dir: Path, silent: bool = False) -> bool:
    """
    Verifica que todos los archivos (.gguf) mencionados en los argumentos del perfil existan.
    """
    missing_files = []
    args = profile.get("args", [])
    
    for i, arg in enumerate(args):
        # Detectamos rutas: argumentos que terminan en .gguf o que siguen a flags conocidos de archivos
        is_path = False
        if isinstance(arg, str) and arg.endswith(".gguf"):
            is_path = True
        elif i > 0 and args[i-1] in ["-m", "--model", "--mmproj"]:
            is_path = True
            
        if is_path:
            path = Path(arg)
            full_path = path if path.is_absolute() else base_dir / path
            if not full_path.exists():
                missing_files.append(str(full_path))
    
    if missing_files:
        if not silent:
            log.error(f"✗ Error en perfil '{profile_key}': No se encontraron archivos críticos:")
            for f in missing_files:
                log.error(f"  - {f}")
        return False
    return True

def validate_all_profiles(config: dict):
    """Valida todos los perfiles al inicio y muestra un resumen."""
    base_dir = Path(config["base_dir"])
    valid_count = 0
    total_count = len(config["profiles"])
    
    log.info("Validando rutas de modelos en perfiles...")
    for key, profile in config["profiles"].items():
        if validate_profile_paths(key, profile, base_dir, silent=True):
            valid_count += 1
        else:
            log.warning(f"  [!] Perfil '{key}' incompleto: faltan archivos de modelo.")
    
    if valid_count == total_count:
        log.info(f"✓ Todos los perfiles ({total_count}) están listos.")
    else:
        log.warning(f"⚠ Solo {valid_count}/{total_count} perfiles están listos para usarse.")

config = load_config()

# BASE_DIR se crea desde el config cargado (ya con llama_exe_path detectada si era necesario)
BASE_DIR = Path(config["base_dir"])
LLAMA_EXE = str(BASE_DIR / config["llama_exe_path"])
ROUTER_PORT = config["router_port"]
BACKEND_PORT = config["backend_port"]
STARTUP_TIMEOUT = config["startup_timeout"]
PROFILES = config["profiles"]
MODEL_ALIASES = config["model_aliases"]

# Validar perfiles al cargar
validate_all_profiles(config)

state = {
    "process":      None,
    "profile_key":  None,
    "loading":      False,
    "start_time":   time.time(),
}

metrics = {
    "profile_usage": {},
    "load_times": {},
    "errors": {
        "timeouts": 0,
        "proxy_errors": 0
    }
}
switch_lock = asyncio.Lock()
BACKEND_URL = f"http://127.0.0.1:{BACKEND_PORT}"

# ─────────────────────────────────────────────────────────────
#  GESTION DE PROCESO
# ─────────────────────────────────────────────────────────────
def kill_backend():
    proc = state["process"]
    if proc and proc.poll() is None:
        log.info("Deteniendo backend (PID %d)...", proc.pid)
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
        log.info("Backend detenido.")
    state["process"] = None
    state["profile_key"] = None

async def wait_for_backend(timeout: int) -> bool:
    deadline = time.time() + timeout
    async with aiohttp.ClientSession() as session:
        while time.time() < deadline:
            try:
                async with session.get(f"{BACKEND_URL}/health", timeout=aiohttp.ClientTimeout(total=2)) as r:
                    if r.status == 200:
                        return True
            except Exception:
                pass
            await asyncio.sleep(1)
    return False

async def switch_profile(profile_key: str):
    async with switch_lock:
        if state["profile_key"] == profile_key and state["process"] and state["process"].poll() is None:
            return

        profile = PROFILES.get(profile_key)
        if not profile:
            log.error(f"Perfil no encontrado: {profile_key}. Usando default.")
            profile_key = "default"
            profile = PROFILES["default"]

        log.info("Cambiando a perfil: %s", profile["description"])

        # Actualizar contador de uso
        metrics["profile_usage"][profile_key] = metrics["profile_usage"].get(profile_key, 0) + 1

        # VALIDACIÓN DE RUTAS ANTES DE ARRANCAR
        if not validate_profile_paths(profile_key, profile, BASE_DIR):
            log.error(f"✗ No se pudo cambiar al perfil '{profile_key}' debido a archivos faltantes.")
            return

        kill_backend()
        state["loading"] = True
        start_load = time.time()

        # Process args to handle paths relative to BASE_DIR
        resolved_args = []
        for i, arg in enumerate(profile["args"]):
            # Si el argumento termina en .gguf o sigue a un flag de ruta, lo convertimos a absoluta
            if isinstance(arg, str) and (arg.endswith(".gguf") or (i > 0 and profile["args"][i-1] in ["-m", "--model", "--mmproj"])):
                path = Path(arg)
                resolved_args.append(str(path if path.is_absolute() else BASE_DIR / path))
            else:
                resolved_args.append(str(arg))

        cmd = [str(LLAMA_EXE)] + resolved_args + [
            "--host", "127.0.0.1",
            "--port", str(BACKEND_PORT),
            "-a", profile_key,
        ]

        log.info("Arrancando: %s", profile["description"])
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(BASE_DIR),
        )
        state["process"] = proc
        state["profile_key"] = profile_key

        log.info("Esperando que el backend este listo (hasta %ds)...", STARTUP_TIMEOUT)
        ok = await wait_for_backend(STARTUP_TIMEOUT)
        state["loading"] = False
        duration = time.time() - start_load

        if ok:
            log.info("Backend listo: %s en :%d (tardó %.2fs)", profile["description"], BACKEND_PORT, duration)
            # Guardar tiempo de carga
            if profile_key not in metrics["load_times"]:
                metrics["load_times"][profile_key] = {"last": 0, "avg": 0, "count": 0}
            
            m = metrics["load_times"][profile_key]
            m["last"] = duration
            m["avg"] = (m["avg"] * m["count"] + duration) / (m["count"] + 1)
            m["count"] += 1
        else:
            log.error("Timeout arrancando backend para perfil '%s'", profile_key)
            metrics["errors"]["timeouts"] += 1
            kill_backend()

# ─────────────────────────────────────────────────────────────
#  PROXY HTTP
# ─────────────────────────────────────────────────────────────
def resolve_profile(model_name: str) -> str:
    if not model_name:
        return "default"
    key = model_name.lower().strip()
    return MODEL_ALIASES.get(key, "default")

async def proxy_request(request: web.Request) -> web.StreamResponse:
    body_bytes = await request.read()
    profile_key = "default"
    
    if body_bytes:
        try:
            payload = json.loads(body_bytes)
            model_name = payload.get("model", "")
            profile_key = resolve_profile(model_name)
        except Exception:
            pass

    await switch_profile(profile_key)

    if not state["process"] or state["process"].poll() is not None:
        return web.Response(status=503, text="Backend no disponible")

    target_url = f"{BACKEND_URL}{request.path_qs}"
    headers = {k: v for k, v in request.headers.items()
               if k.lower() not in ("host", "content-length")}

    timeout = aiohttp.ClientTimeout(total=600, connect=10)
    connector = aiohttp.TCPConnector()

    try:
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            async with session.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=body_bytes,
            ) as backend_resp:

                response = web.StreamResponse(
                    status=backend_resp.status,
                    headers={k: v for k, v in backend_resp.headers.items()
                             if k.lower() not in ("transfer-encoding",)},
                )
                await response.prepare(request)

                async for chunk in backend_resp.content.iter_any():
                    await response.write(chunk)

                await response.write_eof()
                return response

    except aiohttp.ClientError as e:
        log.error("Error proxy: %s", e)
        metrics["errors"]["proxy_errors"] += 1
        return web.Response(status=502, text=f"Error de proxy: {e}")

async def handle_status(request: web.Request) -> web.Response:
    profile_key = state["profile_key"] or "ninguno"
    profile_desc = PROFILES.get(profile_key, {}).get("description", "—")
    pid = state["process"].pid if state["process"] else None
    return web.json_response({
        "router": "AI_MODEL_ROUTER",
        "active_profile": profile_key,
        "description": profile_desc,
        "pid": pid,
        "loading": state["loading"],
        "backend_port": BACKEND_PORT,
    })

async def handle_metrics(request: web.Request) -> web.Response:
    uptime = time.time() - state["start_time"]
    return web.json_response({
        "uptime_seconds": round(uptime, 2),
        "profile_usage": metrics["profile_usage"],
        "load_times": {k: {
            "last_seconds": round(v["last"], 2),
            "avg_seconds": round(v["avg"], 2),
            "count": v["count"]
        } for k, v in metrics["load_times"].items()},
        "errors": metrics["errors"]
    })

# ─────────────────────────────────────────────────────────────
#  ARRANQUE
# ─────────────────────────────────────────────────────────────
async def on_shutdown(app):
    log.info("Apagando router...")
    kill_backend()

def main():
    log.info("=" * 60)
    log.info("  Roo Router arrancando en http://0.0.0.0:%d", ROUTER_PORT)
    log.info("  Backend interno en http://127.0.0.1:%d", BACKEND_PORT)
    log.info("=" * 60)
    log.info("Perfiles disponibles: %s", ", ".join(PROFILES.keys()))
    log.info("Configura RooCode apuntando a http://localhost:%d", ROUTER_PORT)
    log.info("-" * 60)

    app = web.Application(client_max_size=100 * 1024 * 1024)
    app.router.add_get("/_router/status", handle_status)
    app.router.add_get("/_router/metrics", handle_metrics)
    app.router.add_route("*", "/{path_info:.*}", proxy_request)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host="0.0.0.0", port=ROUTER_PORT, print=None)

if __name__ == "__main__":
    main()
