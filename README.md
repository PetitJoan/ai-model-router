# AI Model Router

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

**Intelligent proxy for RooCode that dynamically manages multiple AI models in llama.cpp**

[Español (LEEME.md)](./LEEME.md)

</div>

## 🎯 What is AI Model Router?

**AI Model Router** is a lightweight HTTP proxy written in Python that acts as an intermediary between the **RooCode** development extension and your local **llama.cpp** AI server.

### The Problem It Solves

RooCode has different working "modes" (Architect, Code, Ask, Debug, etc.). Ideally, you want to use a heavy reasoning model (e.g., 27B/35B) for architecture and coding tasks, but a lighter, faster model (e.g., 9B) for quick questions or debugging.

If you have a home PC, **you cannot load all those models into your graphics card's VRAM at the same time.**

**AI Model Router solves this by:**

1. Listening to RooCode requests.
2. Identifying which "mode" is being used.
3. If the required model isn't loaded, it **stops the current llama.cpp server (freeing VRAM)**.
4. **Immediately starts a new server** with the specific model and configuration required.
5. Waits for the new model to load and redirects the request without RooCode losing the connection.

## ✨ Key Features

- 🔄 **Dynamic Model Switching**: Switch between models based on RooCode's mode without manual restarts.
- 🛡️ **Proactive Path Validation**: Automatically checks if `.gguf` files and the `llama-server` executable exist before attempting to switch, preventing "broken" states.
- 📊 **Real-time Observability**: Dedicated endpoint `/_router/metrics` to track load times, profile usage, and error rates.
- 🚀 **Auto-detection**: Smart search for `llama-server.exe` in your base directory.
- 🔧 **Flexible Configuration**: Define multiple model profiles with custom parameters (thinking mode, flash attention, etc.).
- 🌐 **OpenAI Compatible API**: Works seamlessly with any client expecting an OpenAI-like API.

## 📋 Prerequisites

- **Python 3.8** or higher.
- **[llama.cpp](https://github.com/ggerganov/llama.cpp)** installed on your machine.
- AI models in `.gguf` format downloaded locally.
- `aiohttp` (will be automatically installed on the first run).

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-model-router.git
cd ai-model-router
```

### 2. Configure

Copy the example configuration file:

```bash
cp config.example.json config.json
```

Edit `config.json` to match your local paths:
- Set `base_dir` to your llama.cpp folder.
- Update model paths in the `profiles` section.

### 3. Run the Router

**Windows:**
```bash
INICIAR-AI_MODEL_ROUTER.bat
```

**Terminal:**
```bash
python AI_MODEL_ROUTER.py
```

## 🛠️ Configuration (`config.json`)

| Field | Description |
|-------|-------------|
| `base_dir` | Primary path where `llama.cpp` is installed. |
| `llama_exe_path` | Path to the `llama-server` executable (can be relative to `base_dir`). |
| `router_port` | Port where RooCode will connect (default: `8080`). |
| `startup_timeout` | Max seconds to wait for a model to load (default: `120`). |
| `profiles` | Definition of available model profiles and their `llama-server` arguments. |

### Smart Path Resolution
The router automatically resolves relative paths in your `profiles` arguments. If a path ends in `.gguf` or follows `-m`/`--model`, it will be searched within your `base_dir`.

## 🌍 Ecosystem & Resources

This project is part of a powerful local AI development stack. Here are the core components:

*   **[RooCode](https://github.com/RooCodeAI/RooCode)**: An advanced AI coding assistant for VS Code that supports multiple specialized modes (Architect, Code, etc.).
*   **[llama.cpp](https://github.com/ggerganov/llama.cpp)**: The industry-standard C++ implementation for high-performance LLM inference.
*   **[Hugging Face GGUF Models](https://huggingface.co/models?search=gguf)**: The best place to find pre-quantized models ready for use with this router.

## 🛠️ Advanced Configuration Deep Dive

The example configurations in this project aren't arbitrary. They are optimized for modern hardware (tested on 16GB+ VRAM):

### Key Optimization Flags Explained:

| Flag | Purpose | Why use it? |
|------|---------|-------------|
| `-ngl 99` | GPU Offloading | Forces all model layers into VRAM for maximum speed. |
| `--flash-attn` | Flash Attention | Significantly reduces memory usage and speeds up processing for long contexts. |
| `--cache-type-k q4_0` | KV Cache Quantization | Reduces VRAM consumption of the context window, allowing for larger models or longer chats. |
| `--chat-template-kwargs '{"enable_thinking":true}'` | Reasoning Mode | Specifically for Qwen/DeepSeek models to enable the "thinking" process during generation. |

## 💡 Best Practices & Optimization Tips

To get the most out of your local LLMs, follow these community-proven recommendations:

### 1. The Quantization "Sweet Spot"
Don't use 16-bit or even 8-bit models unless you have massive VRAM. For most use cases:
*   **Q4_K_M**: The gold standard. Minimal intelligence loss (~0.1-0.2% perplexity) for a 50% reduction in size.
*   **Q5_K_M / Q6_K**: Use these for reasoning models (Architect mode) if you have the extra VRAM.
*   **Avoid Q2/Q3**: These models "hallucinate" significantly more, especially in coding tasks.

### 2. Hardware-Specific Recommendations

| VRAM | Recommended Model | Suggested `-ngl` | Context (`-c`) |
|------|-------------------|------------------|----------------|
| **8 GB** | 7B - 9B (Q4_K_M) | 40 - 60 | 8k - 16k |
| **12 GB** | 12B - 14B (Q4_0) | 60 - 80 | 16k - 24k |
| **16 GB** | 27B (Q3_K_M/Q4_0) | 99 (Full) | 32k |
| **24 GB+** | 35B+ (Q4_K_M) | 99 (Full) | 32k - 64k |

### 3. Syncing Context with RooCode
If you set `-c 32768` in your `config.json`, configure RooCode's **Context Window** to **~30,000**. This safety margin prevents the "Context Overflow" errors that can crash the inference or make the model forget the beginning of the chat.

### 4. VRAM Monitoring
While the router is switching models, keep an eye on your VRAM usage.
*   **Windows**: Task Manager -> Performance -> GPU -> Dedicated GPU Memory.
*   **Linux/Windows**: Run `nvidia-smi -l 1` in a separate terminal to see real-time allocation.

## 🎓 Learning More: Custom Models & Quantization

If you want to move beyond pre-made models and create your own optimized versions:

1.  **Model Conversion**: Learn how to use `convert_hf_to_gguf.py` in the [llama.cpp scripts directory](https://github.com/ggerganov/llama.cpp/tree/master/convert_hf_to_gguf.py).
2.  **Quantization Guide**: Check the [llama.cpp quantization documentation](https://github.com/ggerganov/llama.cpp#quantization) to understand the trade-offs between model size (Q4, Q8, etc.) and intelligence.
3.  **GGUF Format**: Read about the [GGUF specification](https://github.com/ggerganov/llama.cpp/blob/master/docs/gguf.md) to understand why it's the most efficient format for local LLMs.

## 📊 Monitoring & Metrics

The router provides two main internal endpoints:

- **Status**: `http://localhost:8080/_router/status` - Current active profile and process ID.
- **Metrics**: `http://localhost:8080/_router/metrics` - Detailed stats:
  - **Uptime**: How long the router has been running.
  - **Profile Usage**: Request count per profile.
  - **Load Times**: Last load duration and average load time per model.
  - **Error Tracking**: Counter for timeouts and proxy errors.

## 🔌 Step-by-Step Setup in Roo Code

To ensure Roo Code communicates correctly with the Router and takes advantage of dynamic model switching, follow these steps:

### 1. Open Roo Code Settings
Click the **Gear (Settings)** icon at the bottom of the Roo Code extension panel in VS Code.

### 2. Configure the Provider
In the settings panel, locate and configure the following fields:

- **Provider**: Select `OpenAI Compatible`.
- **Base URL**: Enter `http://localhost:8080/v1` (make sure to include the `/v1` at the end).
- **API Key**: You can enter any text (e.g., `local-router`). The router does not validate it, but Roo Code requires it.
- **Model ID**: Enter the name of the profile you want to use. **It must exactly match** one of the `model_aliases` defined in your `config.json`.
    - *Common examples:* `qwen3.5-orchestrator`, `qwen3.5-architect`, `qwen3.5-code`.

### 3. Adjust the Context Window
- **Max Context Window**: This should match (or be slightly lower than) the `-c` parameter defined in your `config.json` profiles.
    - *Recommendation:* If the router has `-c 32768`, set it to `30000` in Roo Code to leave a safety margin.

### 4. Use Settings Profiles (Recommended)
Roo Code allows you to save **Settings Profiles**. We recommend creating one for each main task:

1.  Configure Roo Code for **Architect** mode (using the `qwen3.5-architect` ID).
2.  Click the profile selector in Roo Code (at the top of the settings) and choose **"Save as new profile..."**.
3.  Name it something like `Roo-Architect`.
4.  Repeat the process for `Roo-Code` (using the `qwen3.5-code` ID).

**How does dynamic switching work?**
When you switch profiles in Roo Code or manually change the "Model ID" in the settings, the Router will detect the change in the next request. If the requested model differs from the one currently loaded, the Router will stop the previous server and automatically load the new one. **You will notice a brief delay in the initial response while the model loads into VRAM.**

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---
**Built with ❤️ for the AI development community.**
