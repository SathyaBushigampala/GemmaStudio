# 3. System Architecture and Workflow

**Project Name:** GemmaStudio  
**Hackathon Track:** Best Use of Gemma 4 (MLH & Google Build with Gemma)  

---

## 1. High-Level System Architecture

GemmaStudio employs a decoupled client-server architecture designed for local development simplicity and enterprise-grade cloud inference:

```
+-------------------------------------------------------------------------+
|                              CLIENT (Browser)                           |
|  - Vanilla JS ES6+ UI Controller (app.js)                              |
|  - Marked.js (Markdown Engine) + DOMPurify 3.0.8 (XSS Sanitizer)        |
|  - Dynamic Syntax Highlighting (Highlight.js)                           |
|  - Thinking Process Visualizer & Benchmark Suite Dashboard               |
+-------------------------------------------------------------------------+
                                    |
                    REST / JSON / Base64 Data-URI
                                    v
+-------------------------------------------------------------------------+
|                           FLASK SERVER (app.py)                         |
|  - Payload Size Defense (16MB MAX_CONTENT_LENGTH, 413 Handler)           |
|  - SSL Certificate Auto-Resolver (_configure_ssl with ca_bundle.pem)    |
|  - Safe Image Parser (Pillow verify & convert, 10MB bounds)             |
|  - Session Persistence Engine (history/*.json Disk Store)                |
|  - Static Code AST Validator (ast.parse)                                |
+-------------------------------------------------------------------------+
                                    |
                    Official google-genai SDK (v2.29.0)
                                    v
+-------------------------------------------------------------------------+
|                       GOOGLE GEMINI API (v1beta)                        |
|  - Hosted Gemma Inference Infrastructure                                 |
|  - Supported: gemma-4-26b-a4b-it (MoE) & gemma-4-31b-it (Dense)         |
|  - Native Thinking Tokens Stream & Multimodal Vision Tensor Processing   |
+-------------------------------------------------------------------------+
```

---

## 2. End-to-End Execution Workflow

1. **User Interaction:**
   - The user selects a model (`gemma-4-26b-a4b-it` or `gemma-4-31b-it`), chooses or customizes a system persona, configures thinking mode (`high` or `minimal`), and inputs text or attaches an image.
2. **Client Validation & Dispatch:**
   - `app.js` captures the inputs, packages active conversation history, and sends a POST request to `/api/generate`.
3. **Server-Side Security & Processing:**
   - `app.py` checks request size (blocking payloads $>16$ MB).
   - Validates that the model identifier is within `SUPPORTED_MODELS`.
   - If an image is present, `_parse_data_uri_to_image` validates file size ($<10$ MB), verifies integrity via Pillow, and converts color channels to RGB.
4. **Cloud Model Inference:**
   - The server invokes `client.models.generate_content` via the official `google-genai` SDK using the configured API key.
5. **Thinking & Answer Disentanglement:**
   - The candidate parts returned by Gemini API are partitioned: parts with `part.thought == True` are directed into `thoughts`, while standard content is placed in `text`.
6. **Persistence & UI Render:**
   - The session is saved to `history/<session_id>.json`.
   - The client sanitizes HTML with DOMPurify and renders the response, displaying the Thinking accordion alongside the final answer.
