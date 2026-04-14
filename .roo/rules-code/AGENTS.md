# Code Mode Rules (Non-Obvious Only)

## Project-Specific Patterns
- All code is in a single file: `AI_MODEL_ROUTER.py` (~584 lines). No modular structure.
- Uses `aiohttp` for async HTTP handling - all request handlers are `async def`.
- Configuration loaded from JSON; missing config auto-created with defaults.

## Critical Code Patterns
- **Path resolution**: Relative `.gguf` paths resolved against `BASE_DIR` (`C:\Llama.cpp\`) in `resolve_profile()` function.
- **Process lifecycle**: Backend process tracked in `state["process"]`; must check `proc.poll() is None` before terminating.
- **Lock usage**: `switch_lock` async context manager REQUIRED for all profile switching to prevent race conditions.

## Error Handling Gotchas
- Proxy requests use `aiohttp.ClientSession` with timeout; failures can cause silent hangs without proper try/except.
- Backend kill requires two-step: `proc.terminate()` then `proc.wait(timeout=15)` before `proc.kill()`.
