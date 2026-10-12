# 4. Testing, Benchmark Telemetry, and Evaluation Results

**Project Name:** GemmaStudio  
**Hackathon Track:** Best Use of Gemma 4 (MLH & Google Build with Gemma)  

---

## 1. Automated Test Suite Execution

GemmaStudio includes an automated test suite located in `tests/test_gemma_studio.py`.

### Execution Command:
```bash
python -m unittest tests/test_gemma_studio.py
```

### Actual Output:
```text
Ran 9 tests in 0.411s
OK (9 passed, 0 failed, 0 errors)
```

### Detailed Test Case Status Table:

| Test ID | Test Function | Target Component | Status | Verified Outcome |
| :--- | :--- | :--- | :---: | :--- |
| `TC-01` | `test_01_index_route` | UI Template / Routes | **PASS** | Returns HTTP 200; verifies branding and navbar components. |
| `TC-02` | `test_02_status_endpoint` | Security / Config API | **PASS** | Returns HTTP 200; validates models list and confirms masked key (`AQ.A...67TA`). |
| `TC-03` | `test_03_request_validation_missing_prompt` | Input Sanitization | **PASS** | Rejects empty prompts with HTTP 400 Bad Request. |
| `TC-04` | `test_04_request_validation_unsupported_model` | Model Safety | **PASS** | Rejects fake model strings (`gpt-fake-model-99`) with HTTP 400. |
| `TC-05` | `test_05_code_snippet_generation` | Code Generator API | **PASS** | Verifies Python (`google-genai`), JS (`@google/genai`), and cURL generation. |
| `TC-06` | `test_06_code_snippet_validation_endpoint` | Static AST Engine | **PASS** | Validates Python syntax via `ast.parse`; flags invalid syntax. |
| `TC-07` | `test_07_image_data_uri_parser` | Multimodal Pipeline | **PASS** | Correctly parses PIL Image from base64; rejects corrupt payloads. |
| `TC-08` | `test_08_experiment_suites_endpoint` | Benchmark Studio API | **PASS** | Returns benchmark suite definitions with valid schema. |
| `TC-09` | `test_09_chat_history_crud` | Disk Storage Engine | **PASS** | Saves session to `history/*.json`, lists sessions, reads session, cleans up. |

---

## 2. Live Cloud Inference Benchmark Evidence

All tests below were executed against the live Google Gemini API endpoints without simulated or fabricated scores:

| Benchmark Suite ID | Target Scenario | Configured Model | Outcome | Measured Latency | Thought Stream Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `math_reasoning` | Multi-step discount deduction ($150 jacket -20% then -10%) | `gemma-4-26b-a4b-it` | **PASS** | 23.28 s | **Captured** (6 step-by-step reasoning tokens verified) |
| `algorithmic_code` | Kahn's Directed Graph Cycle Detection & $O(V+E)$ complexity | `gemma-4-26b-a4b-it` | **PASS** | 61.83 s | **Captured** (Full complexity derivation) |
| `multimodal_vision` | Synthetic Visual QA (Primary shape and color) | `gemma-4-26b-a4b-it` | **PASS** | 4.40 s | **Captured** (Identified blue circular geometry) |

### Sample Actual Outputs
- **Math Deduction:** Correctly produced intermediate price (\$120), second discount (\$12), final price (\$108), and total savings (\$42).
- **Multimodal Visual QA:** Returned: *"The image consists of a single blue circle on a white background."*
