# 2. Technology Stack and Implementation

**Project Name:** GemmaStudio  
**Hackathon Track:** Best Use of Gemma 4 (MLH & Google Build with Gemma)  

---

## 1. Verified Technology Stack

| Layer | Technology | Version | Purpose in GemmaStudio |
| :--- | :--- | :--- | :--- |
| **Backend Runtime** | Python | 3.14.0 | Core application server runtime |
| **Web Framework** | Flask | 3.1.3 | REST API routes, template rendering, and error handling |
| **Cross-Origin Handling** | Flask-CORS | 6.0.0 | Secure API request handling across endpoints |
| **Official AI SDK** | `google-genai` | 2.29.0 | Official Google GenAI SDK interfacing with Gemini API |
| **Image Processing** | Pillow (PIL) | 12.3.0 | In-memory verification, format conversion, and image safety |
| **Environment Mgmt** | `python-dotenv` | 1.0.1 | Safe `.env` loading and credential isolation |
| **Markdown Rendering** | Marked.js | CDN | Client-side markdown formatting |
| **Security / XSS** | DOMPurify | 3.0.8 | Complete sanitization of marked HTML prior to DOM insertion |
| **Syntax Highlighting** | Highlight.js | 11.9.0 | Client-side syntax highlighting for code snippets |
| **PDF Generation** | ReportLab | 5.0.1 | Automated generation of comprehensive evaluation reports |
| **Testing Framework** | `unittest` | Built-in | Automated unit and integration test verification |

---

## 2. Gemma Model Integration Details

GemmaStudio connects directly to Google's hosted Gemma models via the official `google-genai` Python SDK.

### Model Identifiers in Use
1. **`gemma-4-26b-a4b-it` (Default & Recommended):**
   - **Architecture:** Mixture-of-Experts (MoE) with 26 Billion total parameters and ~4 Billion active parameters per token.
   - **Characteristics:** High throughput, low latency, full multimodal vision support, and thinking capability.
2. **`gemma-4-31b-it` (Dense / Heavy Reasoning):**
   - **Architecture:** Dense transformer architecture with 31 Billion parameters.
   - **Characteristics:** Maximum reasoning depth, ideal for complex mathematical derivations and algorithmic proofs.

### Request Dispatching & Thinking Mode
In `app.py`, requests are dispatched to `client.models.generate_content`. When thinking mode is requested:
```python
from google.genai import types

config = types.GenerateContentConfig(
    temperature=temperature,
    system_instruction=system_instruction or None,
    thinking_config=types.ThinkingConfig(thinking_level=thinking_level)
)
response = client.models.generate_content(
    model=model_name,
    contents=contents,
    config=config
)
```
GemmaStudio then loops through `response.candidates[0].content.parts`:
- Tokens where `getattr(part, 'thought', False) == True` are parsed as internal reasoning steps.
- Remaining tokens are parsed as the final answer.

---

## 3. Key Modules and Responsibilities

- **`app.py`:**
  - Manages Windows/Avast SSL trust configuration (`_configure_ssl`).
  - Enforces 16MB maximum payload limit via `MAX_CONTENT_LENGTH`.
  - Implements image parser `_parse_data_uri_to_image` with 10MB bounds and format conversion.
  - Exposes REST endpoints: `/api/status`, `/api/generate`, `/api/code-snippet`, `/api/history/*`, and `/api/experiments/*`.
- **`static/js/app.js`:**
  - Manages UI events, session state, debounced search filtering, and model switching.
  - Sanitizes markdown with `DOMPurify.sanitize(marked.parse(...))`.
  - Powers the interactive Experiment Studio and benchmark runner.
- **`templates/index.html`:**
  - Semantic HTML5 layout featuring sidebar controls, history drawer, and modals.
- **`tests/test_gemma_studio.py`:**
  - Automated test suite covering endpoints, validation logic, parser safety, and history CRUD.
