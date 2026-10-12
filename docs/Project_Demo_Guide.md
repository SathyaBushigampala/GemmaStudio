# 5. Project Demo and Evaluation Guide

**Project Name:** GemmaStudio  
**Hackathon Track:** Best Use of Gemma 4 (MLH & Google Build with Gemma)  

---

## 1. Quick Start Installation & Execution

### Prerequisites:
- Python 3.10+ (Tested on Python 3.14.0 64-bit on Windows)
- Google Gemini API Key (Obtainable at [Google AI Studio](https://aistudio.google.com/apikey))

### Setup Commands:
```bash
# 1. Clone or navigate to the repository folder
cd Hacktoberfest

# 2. Install required dependencies
pip install -r requirements.txt

# 3. Create or check .env configuration (or enter key via UI Settings)
# GEMINI_API_KEY=your_actual_gemini_api_key

# 4. Start the application server
python app.py
```

The studio is immediately available at **`http://localhost:5000`** (or `http://127.0.0.1:5000`).

---

## 2. Step-by-Step Evaluator Demo Walkthrough

### Step 1: Model Selection & Thinking Mode Verification
1. Open the homepage at `http://localhost:5000`.
2. Notice the active model badge: `gemma-4-26b-a4b-it`.
3. In the sidebar, select **High Reasoning** under Thinking Mode.
4. Click the welcome hero card **"Thinking Process"** or type:
   > *"If a box contains 3 red balls and 5 blue balls, what is the probability of drawing two red balls without replacement? Show your step-by-step thinking."*
5. Submit the query.
6. **Observation:** A styled accordion labeled **"🧠 Gemma's Internal Thinking Process"** appears above the answer, showing the exact planning tokens before the final probability ($\frac{3}{28}$) is displayed.

### Step 2: Multimodal Image Understanding
1. Click the **"Vision Understanding"** card or use the image upload button (`+` icon next to chat input).
2. Attach any image, diagram, or chart (PNG, JPEG, WebP).
3. Ask: *"What is depicted in this image? Explain the key elements."*
4. **Observation:** GemmaStudio safely parses the image via Pillow and returns visual insights grounded in the image content.

### Step 3: Generated Code Snippet Validation
1. Click the **`<>` (Code Snippets)** button in the chat interface.
2. Toggle between **Python (`google-genai`)**, **JavaScript (`@google/genai`)**, and **cURL**.
3. Notice that the snippet precisely reflects your current model, thinking level, and prompt parameters.

### Step 4: The Benchmark Studio (High-Value Feature)
1. In the top navbar, click **"🧪 Experiment Studio"**.
2. Select a benchmark suite from the dropdown:
   - *Mathematical Reasoning & Deductive Proof*
   - *Algorithmic Complexity & Cycle Detection*
   - *Kyoto Tea Master Persona Compliance*
   - *Multimodal Visual Geometry & Color QA*
3. Click **"Run Benchmark Suite"**.
4. Watch the live progress indicator as GemmaStudio queries Google's Gemini API, measures real token latency in milliseconds, and validates test criteria.
5. Click **"Export Markdown Report"** or **"Export JSON"** to download the evaluation file for presentation or archival.

### Step 5: ChatGPT-Style Searchable History
1. Click the **History** tab in the sidebar.
2. Inspect past sessions loaded from disk (`history/*.json`).
3. Type keywords in the search bar (e.g., "probability" or "graph") to see debounced real-time filtering across titles and responses.
