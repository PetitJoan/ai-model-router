# Debug Mode Rules (Non-Obvious Only)

## Critical Debug Patterns
- **Silent hangs**: Proxy requests with `aiohttp.ClientSession` can hang silently without proper try/except blocks.
- **Process state check**: Always verify `proc.poll() is None` before attempting to terminate backend process.
- **Two-step kill**: Backend termination requires `proc.terminate()` followed by `proc.wait(timeout=15)`, then `proc.kill()` on timeout.

## Metrics Endpoints
- `/_router/metrics`: Returns uptime, profile usage stats, load times, error counts per profile
- `/_router/status`: Returns active profile name, backend PID, loading state

## Common Debug Scenarios
- **Invalid profiles**: Missing `.gguf` files cause startup failure - validate paths before starting
- **Race conditions**: Profile switching without `switch_lock` can corrupt state
- **Path resolution errors**: Relative `.gguf` paths must be resolved against `C:\Llama.cpp\`
