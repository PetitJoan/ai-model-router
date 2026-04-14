# Ask Mode Rules (Non-Obvious Only)

## Documentation Context
- **Single-file architecture**: All router logic is in `AI_MODEL_ROUTER.py` (~584 lines) - no modular structure to navigate.
- **Configuration auto-creation**: Missing `config.json` is automatically created with defaults on first run.
- **Auto-detection behavior**: Router finds `llama-server.exe` automatically if path is empty in config.

## Key Endpoints for Questions
- `/_router/status`: Current active profile, backend PID, loading state
- `/_router/metrics`: Uptime, profile usage statistics, load times, error counts

## Counterintuitive Patterns
- Profile args with `-m/--model` flags need path resolution if relative paths are used.
- Backend startup has 120s timeout before failing - not immediate failure.
- `.gguf` path validation happens at startup, not lazily on first request.
