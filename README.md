# 🚀 AI Model Router for RooCode + llama.cpp (v2.0)

**AI Model Router** is an intelligent Python proxy that acts as an optimized intermediary between the **RooCode** extension and the local **llama.cpp** server.

Designed specifically for managing powerful models (Qwen 27B/35B) on machines with limited VRAM, enabling a smooth experience with massive memory.

---

## 🌟 Key Features (v2.0)

### 1. 🧠 Bidirectional Dynamic Context Management
The router analyzes every Roo Code request and adjusts the server in real-time:
*   **Auto-Expansion:** if the conversation grows, the router restarts the server expanding the context window (up to 128k). No more "context size exceeded" errors!
*   **Auto-Shrink:** if you clear the chat or start a small task, the router reduces the context to the base value (64k). This frees up VRAM and significantly speeds up model responses.

### 2. 👁️ Intelligent Vision Support (MCP)
Optimized for working with screenshot tools (MCP) and CSS:
*   Automatically detects images in the request payload.
*   Adds a safety token margin (3000 tokens per image) to prevent crashes when processing web screenshots.

### 3. ⚡ Non-Blocking Architecture
Implements an asynchronous event system (`boot_event`) that prevents Roo Code from "hanging" while the model loads into VRAM. Requests wait their turn without breaking the connection.

---

## 🛠️ Requirements & Installation

### Requirements
*   **Python 3.10+**
*   **llama.cpp** (with `llama-server.exe`) installed.
*   **Dependencies:** `aiohttp` (the router will auto-install it if missing).

### Quick Start
1. Clone or download this repository.
2. Ensure your `.gguf` models are in your llama.cpp folder.
3. Run the router:
   ```powershell
   python AI_MODEL_ROUTER.py
   ```

---

## ⚙️ Roo Code Configuration

1.  **Provider:** `OpenAI Compatible`
2.  **Base URL:** `http://localhost:8080`
3.  **API Key:** `any`
4.  **Model ID:** Choose a profile:
    *   `architect` / `orchestrator` / `code` / `ask`

---

## 📊 Console Feedback (CMD)
*   **`--> architect (~45000 tokens)`**: Incoming request size.
*   **`⚠ REINICIO DINAMICO`**: Visual warning of context expansion or shrinkage.
*   **`✓ Listo en 12.5s`**: Server ready confirmation.

---
*Developed to provide maximum freedom and power for local AI software development.*
