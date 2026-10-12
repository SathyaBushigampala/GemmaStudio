# 🌟 GemmaStudio | Complete Project Documentation

> **Official Track:** MLH & Google "Build with Gemma" — Hacktoberfest  
> **Official Docs Reference:** [Run Gemma with the Gemini API](https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api)  
> **Repository Name:** GemmaStudio  

---

## 📑 Table of Contents
1. [Project Overview](#-project-overview)
2. [What is Gemma on Gemini API?](#-what-is-gemma-on-gemini-api)
3. [Model Identification Breakdown](#-model-identification-breakdown)
4. [Key Features & Capabilities](#-key-features--capabilities)
5. [Architecture & Workflow](#-architecture--workflow)
6. [Complete Codebase File Breakdown](#-complete-codebase-file-breakdown)
7. [Installation & Setup Guide](#-installation--setup-guide)
8. [How to Run GemmaStudio](#-how-to-run-gemmastudio)
9. [UI Walkthrough & Controls](#-ui-walkthrough--controls)
10. [API Code Reference (Python, JS, cURL)](#-api-code-reference)
11. [Hackathon Submission & Evaluation Checklist](#-hackathon-submission--evaluation-checklist)
12. [Troubleshooting & FAQ](#-troubleshooting--faq)

---

## 🚀 Project Overview

**GemmaStudio** is a full-stack, developer-focused web playground and studio designed specifically for exploring and building with Google's **Gemma 4** open-weights models hosted directly on the **Google Gemini API**.

Traditionally, running Gemma models required either:
- Large GPUs with complex local environments (Ollama, vLLM, HuggingFace, PyTorch), or
- Cloud container deployments on Vertex AI / GKE.

With **Gemma on Gemini API**, developers get the best of both worlds:
- **No local GPU required**: Google hosts the inference servers.
- **Official SDK Integration**: Access Gemma using the unified `google-genai` SDK.
- **Advanced Capabilities**: Full support for **Thinking Mode** (step-by-step reasoning), **Multimodal Vision** (image analysis), **System Personas**, and **Multi-turn Chat**.

---

## 🤖 What is Gemma on Gemini API?

Google's Gemini API provides hosted access to Gemma models via a unified programming interface. This eliminates infrastructure overhead and provides instant, scalable generative AI capabilities for prototyping and production.

### Core Differences vs Traditional Local Gemma:
| Attribute | Gemma on Gemini API (This Project) | Local Gemma (Ollama/PyTorch) |
| :--- | :--- | :--- |
| **Hardware Needed** | Any PC / Laptop (Zero GPU requirement) | High-end GPU (16GB - 64GB VRAM) |
| **Setup Time** | 1 minute (Install SDK & paste API key) | Hours of downloading weights & drivers |
| **Model Version** | Gemma 4 (26B MoE & 31B Dense) | Often limited to smaller 2B / 7B / 9B variants |
| **Multimodal Vision** | Built-in native support | Requires separate vision pipeline setup |
| **Reasoning / Thinking** | Native toggle (`high` / `minimal`) | Complex custom prompt templates |

---

## 🔍 Model Identification Breakdown

In the studio header, you will see model identifiers like **`gemma-4-26b-a4b-it`**. Here is the breakdown:

```
 gemma  -  4  -  26b  -  a4b  -  it
   │       │      │       │      │
   │       │      │       │      └── Instruction-Tuned (fine-tuned for chat & tasks)
   │       │      │       └──────── Active 4 Billion parameters (MoE architecture)
   │       │      └──────────────── Total Model Size: 26 Billion parameters
   │       └─────────────────────── Model Generation: 4
   └─────────────────────────────── Google Gemma Family
```

### Supported Models:
1. **`gemma-4-26b-a4b-it` (Recommended / Default)**:
   - Mixture-of-Experts (MoE) architecture.
   - Total weights: 26B, but only ~4B are activated per token.
   - Ultra-low latency, blazing fast generation, vision support.
2. **`gemma-4-31b-it` (Dense / Heavy Reasoning)**:
   - 31 Billion dense parameters.
   - Maximized reasoning capacity for advanced mathematics, complex algorithm proofs, and deep analytical logic.

---

## ⚡ Key Features & Capabilities

### 1. 🧠 Interactive Thinking Process Visualizer
Gemma 4 introduces an internal reasoning mechanism. GemmaStudio captures this reasoning stream and surfaces it in an interactive accordion (`🧠 Gemma's Internal Thinking Process`). You can inspect how the model planned its response before writing the final output.
- **High Reasoning**: Set `thinking_level="high"` for complex logic, algorithms, and math.
- **Minimal**: Set `thinking_level="minimal"` for instant, conversational responses.

### 2. 👁️ Multimodal Vision Understanding
Upload, drag & drop, or paste images directly into the chat:
- Diagram and flowchart interpretation.
- Code screenshot debugging.
- Image captioning and scene description.
- Automatically converts uploads to base64 `types.Part.from_bytes` payloads.

### 3. 🎭 System Personas & Behavioral Control
Includes presets and custom instructions:
- **Kyoto Tea Master**: Speaks calmly and poetically with nature metaphors (straight from Google's official documentation).
- **Senior Code Architect**: Focuses on clean architecture, asymptotic time/space complexity, and edge cases.
- **Math & Proofs Tutor**: Rigorous step-by-step mathematical deduction.
- **Custom Persona**: User-defined instructions.

### 4. 💻 Dynamic Code Snippet Generator
Click the `<>` icon to inspect the exact, working code required to replicate your prompt, thinking mode, and persona in:
- **Python** (`google-genai` SDK)
- **JavaScript / TypeScript** (`@google/genai` package)
- **cURL** (REST API)

### 5. 🔍 ChatGPT-Style Search History & Developer Disk Storage
- **ChatGPT-Style Sidebar**: Switch between Controls and History with real-time session counter badge.
- **Instant Search Bar**: Filter past queries and answers in real-time across titles, prompts, and assistant responses.
- **Disk Persistence for Developers**: Every session is automatically saved to the `history/` directory on disk as structured JSON files (`history/<session_id>.json`). Developers can inspect past searches, model latency, prompts, and reasoning thoughts directly from their IDE.
- **One-Click Session Restoration**: Clicking any past session restores the full multi-turn conversation, thinking accordions, and model settings.
- **Session Management**: Rename, delete individual chats, or clear all history with one click.
- **Markdown Export**: Download any active chat session as GitHub-flavored Markdown.

### 6. 🧪 Gemma Experiment & Code Validation Studio (Hackathon Special)
Access via the top navigation bar **"🧪 Experiment Studio"**:
- **Repeatable Test Suites**: Execute predefined benchmarks across mathematical reasoning, Kahn's algorithm graph coding, persona constraint compliance, and synthetic multimodal vision QA.
- **Live Latency & Reasoning Telemetry**: Tracks real inference duration (ms) and thought tokens returned by the Gemini API.
- **Static Code Validation**: Instant AST syntax check for Python and schema validation for JS snippets via `/api/experiments/validate-code`.
- **Judge Audit Export**: Download complete test execution logs as Markdown or JSON reports.

### 7. 🔐 Security & Hardening
- **16MB Payload Guard**: Hardware DOS protection with custom 413 error handler.
- **XSS Prevention**: Full DOMPurify sanitization before rendering Markdown responses.
- **Safe Secrets**: Masked API keys (`AQ.A...67TA`) and protected `.env` credentials.
- **In-Memory Image Validation**: PIL image integrity checks with 10MB individual file bounds.

---

## 🏗️ Architecture & Workflow

```mermaid
flowchart TD
    User([User Browser]) <--> |HTTP / JSON / Base64| WebUI["GemmaStudio UI (Templates & Static JS)"]
    WebUI <--> |REST API Endpoints| FlaskServer["Flask Backend (app.py)"]
    FlaskServer <--> |Auth / Configuration| LocalEnv[".env (GEMINI_API_KEY)"]
    FlaskServer <--> |Google GenAI SDK (v2.29)| GoogleAPI["Google Gemini API Cloud"]
    GoogleAPI --> Gemma26B["gemma-4-26b-a4b-it (MoE)"]
    GoogleAPI --> Gemma31B["gemma-4-31b-it (Dense)"]
```

---

## 📂 Complete Codebase File Breakdown

```
Hacktoberfest/
├── app.py                     # Main Flask server with Google GenAI SDK integration
├── requirements.txt           # Python dependencies
├── .env                       # Local secrets (API Key)
├── .env.example               # Template for environment variables
├── run.bat                    # Windows one-click batch script
├── run.ps1                    # PowerShell launcher script
├── README.md                  # Complete documentation (this file)
├── templates/
│   └── index.html             # Single-page web studio HTML structure
└── static/
    ├── css/
    │   └── style.css          # Glassmorphic, dark-mode CSS styling
    └── js/
        └── app.js             # Client-side JavaScript handling interactions
```

### Detailed File Roles:

1. **`app.py`**:
   - Manages API routing (`/`, `/api/status`, `/api/set-key`, `/api/generate`, `/api/code-snippet`).
   - Converts base64 image data into `google.genai.types.Part.from_bytes`.
   - Constructs `types.GenerateContentConfig` with `thinking_config` and `system_instruction`.
   - Separates internal `part.thought` tokens from main text response for visualization.

2. **`templates/index.html`**:
   - Modular layout containing sidebar controls, top navbar, welcome hero, message stream, and modal windows (Settings & Code Snippets).

3. **`static/css/style.css`**:
   - Polished design with dark theme colors (`#0f1117`), Google AI gradients, thinking glow effects, syntax-highlighted code blocks, and responsive mobile adaptations.

4. **`static/js/app.js`**:
   - Handles asynchronous chat submissions, loading state animations, drag-and-drop file readers, marked.js markdown rendering, clipboard copy handlers, and session markdown exports.

5. **`run.bat` & `run.ps1`**:
   - Ensures dependencies are installed quietly and runs `python app.py` with zero configuration required.

---

## 💻 Installation & Setup Guide

### 1. Prerequisites
- **Python**: Version 3.10 or newer (tested on Python 3.14).
- **Gemini API Key**: Obtain a free key from [Google AI Studio](https://aistudio.google.com/apikey).

### 2. Clone or Navigate to the Workspace
```powershell
cd c:\Users\sathy\OneDrive\Documents\Hacktoberfest
```

### 3. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### 4. Configure API Key
Create a `.env` file (or rename `.env.example` to `.env`):
```env
GEMINI_API_KEY=your_google_ai_studio_api_key_here
PORT=5000
```
*(You can also skip this step and enter your key directly in the web app UI!)*

---

## ▶️ How to Run GemmaStudio

### Option 1: Double-Click Runner (Windows)
Double-click `run.bat` in the project folder.

### Option 2: PowerShell
```powershell
.\run.ps1
```

### Option 3: Standard Terminal
```bash
python app.py
```

Once started, open your web browser and go to:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 🖥️ UI Walkthrough & Controls

1. **Top Navbar**:
   - Displays active model identifier (`gemma-4-26b-a4b-it` or `gemma-4-31b-it`).
   - Quick links to Google's official documentation and AI Studio API key generator.
2. **Sidebar Controls**:
   - **Model Dropdown**: Choose between the 26B MoE model and the 31B Dense model.
   - **Thinking Mode**: Switch between **High Reasoning** (detailed chain-of-thought) and **Minimal** (fast generation).
   - **System Persona**: Choose from predefined personas (Kyoto Tea Master, Senior Architect) or write your own custom rules.
   - **Quick Prompts**: One-click demo cards for instant testing.
   - **Footer Tools**: Status indicator, Settings (⚙️), Code Snippet Viewer (`<>`), and Markdown Export (📥).
3. **Chat Arena**:
   - **Message Bubbles**: Clean conversational UI with markdown formatting, inline syntax highlighting, and code copy buttons.
   - **Thinking Accordion**: Collapsible purple box displaying Gemma's raw reasoning steps.
   - **Input Bar**: Attach images via clip icon, drag-and-drop, or `Ctrl+V` clipboard paste.

---

## 📜 API Code Reference

Here is how GemmaStudio connects to Gemma 4 via the Google GenAI SDK:

### Python (`google-genai`)
```python
from google import genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

# 2. Generate Content with Thinking Mode & System Instruction
response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents="Explain why ice floats on liquid water.",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high"),
        system_instruction="You are a university chemistry professor. Be clear and analytical."
    )
)

print(response.text)
```

### JavaScript / TypeScript (`@google/genai`)
```javascript
import { GoogleGenAI, ThinkingLevel } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: "YOUR_GEMINI_API_KEY" });

const response = await ai.models.generateContent({
  model: "gemma-4-26b-a4b-it",
  contents: "Explain why ice floats on liquid water.",
  config: {
    thinkingConfig: { thinkingLevel: ThinkingLevel.HIGH },
    systemInstruction: "You are a university chemistry professor. Be clear and analytical."
  }
});

console.log(response.text);
```

### REST / cURL
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemma-4-26b-a4b-it:generateContent?key=$GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "contents": [{"parts": [{"text": "Explain why ice floats on liquid water."}]}],
    "systemInstruction": {"parts": [{"text": "You are a university chemistry professor."}]},
    "generationConfig": {
      "thinkingConfig": { "thinkingLevel": "high" }
    }
  }'
```

---

## 🏆 Hackathon Submission & Evaluation Checklist

| Hackathon Criterion | How GemmaStudio Fulfills It |
| :--- | :--- |
| **Track Alignment** | Built strictly using the **Gemma on Gemini API** documentation guidelines. |
| **Model Diversity** | Implements both `gemma-4-26b-a4b-it` (MoE) and `gemma-4-31b-it` (Dense). |
| **Feature Completeness** | Thinking mode visualizer, multimodal image analysis, system personas, and multi-turn conversations. |
| **Developer Ergonomics** | Generates instant Python, JS, and cURL snippets for any configured prompt. |
| **Usability & Design** | Sleek glassmorphic dark-mode web interface with zero installation friction. |
| **Portability** | One-click Windows launch scripts (`run.bat`, `run.ps1`) and zero-GPU requirement. |

---

## ❓ Troubleshooting & FAQ

### Q1: What does `status: needs_key` mean?
**A:** You haven't configured a Gemini API key yet. Open the in-app settings (click the **⚙️** icon in the bottom-left) or paste your key into the `.env` file. Free keys can be created at [Google AI Studio](https://aistudio.google.com/apikey).

### Q2: Why is the model called `gemma-4-26b-a4b-it`?
**A:** That is Google's official model ID. It represents Gemma 4, with 26 Billion total parameters, 4 Billion active parameters (MoE architecture), and Instruction Tuning (`it`).

### Q3: Can I run this without an NVIDIA GPU?
**A:** **Yes!** Because inference runs on Google's cloud infrastructure via the Gemini API, this project runs on any standard Windows, Mac, or Linux computer without needing a GPU.

### Q4: How do I change the port?
**A:** Update `PORT=5000` in your `.env` file to your preferred port number.

---

## 📚 Hackathon Documentation & Evaluation Dossier

Complete technical documentation and evaluation evidence are available directly in this repository:

- 📄 **[Evaluation PDF Report](docs/GemmaStudio_Hackathon_Project_Report.pdf)**: Complete 7-page technical dossier with cover page, architecture diagrams, benchmark evidence, security audit, and demo script.
- 📋 **[Evaluator Checklist & Scorecard](docs/Hackathon_Evaluator_Checklist.md)**: 100-point rubric breakdown across all 8 judging criteria.
- 🎯 **[Problem Statement & Solution](docs/Problem_Statement_and_Solution.md)**: In-depth problem analysis and feature matrix.
- ⚙️ **[Technology Stack & Implementation](docs/Technology_Stack_and_Implementation.md)**: SDK signatures, thinking mode parser, and Pillow pipeline.
- 🏗️ **[System Architecture](docs/System_Architecture.md)**: End-to-end data flow and decoupled client-server architecture.
- 🧪 **[Testing & Live Benchmarks](docs/Testing_and_Results.md)**: Automated test suite breakdown and live Gemini API latency measurements.
- 🚀 **[Project Demo Guide](docs/Project_Demo_Guide.md)**: Step-by-step evaluator testing script.

---

## 📄 License
This project is open-source under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.  
All Gemma models are subject to Google's [Gemma Terms of Use](https://ai.google.dev/gemma/terms).
