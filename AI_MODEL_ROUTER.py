"""
AI_MODEL_ROUTER.py  —  Router inteligente para RooCode + llama.cpp
================================================================
Soporte para VISION (MCP) y Contexto Bidireccional
"""

import asyncio
import json
import logging
import re
import subprocess
import sys
import time
from pathlib import Path

def check_dependencies():
    try:
        import aiohttp
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])

check_dependencies()
import aiohttp
from aiohttp import web

CONFIG_FILE = Path(__file__).parent / "config.json"
logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-7s  %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("router")

def find_llama_exe(base_dir: Path) -> str:
    exe_name = "llama-server.exe"
    for item in sorted(base_dir.iterdir(), reverse=True):
        if item.is_dir() and re.match(r"llama-\d+\.\d+-bin-win-.*", item.name):
            exe_path = item / exe_name
            if exe_path.exists(): return str(exe_path.resolve())
    for path in base_dir.rglob(exe_name): return str(path.resolve())
    raise FileNotFoundError("No se encontró llama-server.exe")

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
    if not config.get("llama_exe_path"):
        config["llama_exe_path"] = find_llama_exe(Path(config["base_dir"]))
    return config

config = load_config()
BASE_DIR = Path(config["base_dir"])
LLAMA_EXE = config["llama_exe_path"] if Path(config["llama_exe_path"]).is_absolute() else str(BASE_DIR / config["llama_exe_path"])
ROUTER_PORT = config["router_port"]
BACKEND_PORT = config["backend_port"]
STARTUP_TIMEOUT = config["startup_timeout"]
PROFILES = config["profiles"]
MODEL_ALIASES = config["model_aliases"]

state = {"process": None, "profile_key": None, "current_ctx": 0, "loading": False}
switch_lock = asyncio.Lock()
boot_event = asyncio.Event()
boot_event.set()
BACKEND_URL = f"http://127.0.0.1:{BACKEND_PORT}"

def estimate_tokens_from_payload(payload: dict) -> int:
    tokens = 0
    for m in payload.get("messages", []):
        content = m.get("content", "")
        if isinstance(content, str):
            tokens += int(len(content) / 2.5)
        elif isinstance(content, list):
            for part in content:
                p_type = part.get("type", "")
                if p_type == "text":
                    tokens += int(len(part.get("text", "")) / 2.5)
                elif p_type in ["image_url", "image"]:
                    tokens += 3000 
    return tokens + 1500 + payload.get("max_tokens", 4096)

def get_profile_default_ctx(profile: dict) -> int:
    args = profile.get("args", [])
    for i, arg in enumerate(args):
        if arg in ["-c", "--ctx-size"] and i + 1 < len(args):
            return int(args[i+1])
    return 65536

def kill_backend():
    proc = state["process"]
    if proc and proc.poll() is None:
        log.info("Deteniendo backend...")
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except:
            proc.kill()
    state["process"], state["profile_key"], state["current_ctx"] = None, None, 0

async def wait_for_backend(timeout: int) -> bool:
    deadline = time.time() + timeout
    async with aiohttp.ClientSession() as session:
        while time.time() < deadline:
            try:
                async with session.get(f"{BACKEND_URL}/health", timeout=1) as r:
                    if r.status == 200:
                        return True
            except:
                pass
            await asyncio.sleep(1)
    return False

async def switch_profile(profile_key: str, requested_ctx: int = 0):
    if state["loading"]:
        await boot_event.wait()
    
    async with switch_lock:
        profile = PROFILES.get(profile_key, PROFILES.get("default"))
        default_ctx = get_profile_default_ctx(profile)
        final_ctx = default_ctx
        
        if config.get("auto_expand_context", True) and requested_ctx > default_ctx:
            final_ctx = ((requested_ctx + 8191) // 8192) * 8192
        
        max_limit = config.get("global_max_context", 131072)
        if final_ctx > max_limit:
            final_ctx = max_limit

        need_restart = False
        if state["profile_key"] != profile_key or state["current_ctx"] < final_ctx:
            need_restart = True
        elif state["current_ctx"] > default_ctx and requested_ctx <= (default_ctx * 0.8):
            log.info("📉 Auto-Shrink: Volviendo a contexto base para ganar velocidad.")
            final_ctx = default_ctx
            need_restart = True

        if not need_restart and state["process"] and state["process"].poll() is None:
            return

        log.warning("!" * 60)
        log.warning(f" REINICIO: {profile_key} | CTX: {final_ctx}")
        log.warning("!" * 60)
        
        boot_event.clear()
        state["loading"] = True
        kill_backend()

        resolved_args = []
        p_args = profile.get("args", [])
        ctx_set = False
        i = 0
        while i < len(p_args):
            arg = p_args[i]
            if arg in ["-c", "--ctx-size"]:
                resolved_args.extend([arg, str(final_ctx)])
                ctx_set, i = True, i + 2
            elif isinstance(arg, str) and (arg.endswith(".gguf") or (i > 0 and p_args[i-1] in ["-m", "--model", "--mmproj"])):
                path = Path(arg)
                resolved_args.append(str(path if path.is_absolute() else BASE_DIR / path))
                i += 1
            else:
                resolved_args.append(str(arg))
                i += 1
        
        if not ctx_set:
            resolved_args.extend(["-c", str(final_ctx)])

        cmd = [str(LLAMA_EXE)] + resolved_args + ["--host", "127.0.0.1", "--port", str(BACKEND_PORT)]
        
        start_t = time.time()
        state["process"] = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(BASE_DIR))
        state["profile_key"], state["current_ctx"] = profile_key, final_ctx
        
        ok = await wait_for_backend(STARTUP_TIMEOUT)
        state["loading"] = False
        boot_event.set()
        
        if ok:
            log.info(f"✓ Listo en {time.time()-start_t:.1f}s")
        else:
            log.error("✗ Timeout")
            kill_backend()

async def proxy_request(request: web.Request) -> web.StreamResponse:
    body = await request.read()
    profile_key, tokens = "default", 0
    try:
        payload = json.loads(body)
        profile_key = MODEL_ALIASES.get(payload.get("model", "").lower().strip(), "default")
        tokens = estimate_tokens_from_payload(payload)
        log.info(f"--> {profile_key} (req: ~{tokens} tokens | actual: {state['current_ctx']})")
    except:
        pass

    await switch_profile(profile_key, tokens)
    
    if not state["process"] or state["process"].poll() is not None:
        return web.Response(status=503, text="Offline")

    target_url = f"{BACKEND_URL}{request.path_qs}"
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "content-length")}
    
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=600)) as session:
            async with session.request(request.method, target_url, headers=headers, data=body) as resp:
                proxy_resp = web.StreamResponse(
                    status=resp.status,
                    headers={k: v for k, v in resp.headers.items() if k.lower() not in ("transfer-encoding",)}
                )
                await proxy_resp.prepare(request)
                async for chunk in resp.content.iter_any():
                    await proxy_resp.write(chunk)
                await proxy_resp.write_eof()
                return proxy_resp
    except Exception as e:
        log.error(f"Proxy error: {e}")
        return web.Response(status=502, text=str(e))

async def handle_status(request):
    return web.json_response({
        "profile": state["profile_key"],
        "ctx": state["current_ctx"],
        "loading": state["loading"]
    })

def main():
    print("=" * 65)
    print("  🚀 AI MODEL ROUTER — Soporte para VISION (MCP)")
    print("=" * 65)
    print(f"  Router URL:    http://localhost:{ROUTER_PORT}")
    print(f"  Contexto Base: 64k | Max: 128k")
    print("-" * 65)
    
    app = web.Application(client_max_size=100*1024*1024)
    app.router.add_get("/_router/status", handle_status)
    app.router.add_route("*", "/{path_info:.*}", proxy_request)
    app.on_shutdown.append(lambda app: kill_backend())
    
    web.run_app(app, host="0.0.0.0", port=ROUTER_PORT, print=None)

if __name__ == "__main__":
    main()
