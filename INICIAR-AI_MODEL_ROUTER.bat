@echo off
REM ============================================================
REM  AI MODEL ROUTER — Proxy inteligente para RooCode
REM  Escucha en :8080 y arranca el modelo correcto segun el modo
REM
REM  Modos RooCode → Modelo:
REM    architect  →  27B Thinking
REM    code       →  35B-A3B Thinking
REM    ask        →  27B No-Think
REM    debug      →  27B No-Think
REM    (otros)    →  9B fallback
REM
REM  Requisito: pip install aiohttp
REM ============================================================

title "[Roo Router] :8080"

python AI_MODEL_ROUTER.py

pause
