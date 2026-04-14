# Architect Mode Rules (Non-Obvious Only)

## Hidden Coupling & Architecture Constraints
- **Single-file monolith**: All 584 lines of router logic in `AI_MODEL_ROUTER.py` - no separation of concerns.
- **State management**: Backend process tracked globally in `state["process"]` dict - no isolation between requests.
- **Lock-based concurrency**: Only `switch_lock` async context manager prevents race conditions during profile switching.

## Undocumented Architectural Decisions
- **Startup timeout**: 120s default wait for backend startup before failing (configurable but not exposed).
- **Path resolution strategy**: Relative `.gguf` paths resolved against hardcoded `C:\Llama.cpp\` BASE_DIR.
- **Graceful shutdown**: Two-step kill (`terminate()` → `wait(15)` → `kill()`) required for clean process termination.

## Performance Bottlenecks
- Proxy requests use `aiohttp.ClientSession` per request - potential connection pooling inefficiency.
- Profile switching requires stopping current backend and starting new one (no hot-swapping).
- Metrics tracking is in-memory only - no persistence across restarts.
