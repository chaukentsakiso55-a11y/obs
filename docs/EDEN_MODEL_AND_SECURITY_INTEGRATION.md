# EDEN AI: local inference and security integration

EDEN is the OBSIDIAN assistant and security-explanation layer, **not** the security enforcement authority.

## Local model choices
- Start with quantized Qwen3 0.6B / 1.7B / 4B or another compatible open-weight model, subject to hardware, license and evaluation.
- Ollama is an optional local inference backend, not an EDEN model or a bundled dependency.
- The default runtime selects `qwen3:1.7b` as a candidate; users must download model weights themselves.
- For 8GB RAM, evaluate memory and response latency before changing the default.
- For future independent EDEN model weights, use the same local inference interface but document training provenance and evaluation.

## Current implementation
- `obsidian/eden_runtime.py`: loopback-only Ollama chat API client, response cap, timeout, bounded conversation history and honest fallback.
- `obsidian/security_events.py`: permission inspection, deterministic event classification, JSONL audit append.
- `obsidian/eden.py`: independent deterministic ALLOW/REVIEW/BLOCK policy.

## Security constraints
- No shell command execution through model output.
- No model-generated security decision automatically enforced.
- No external endpoint by default.
- Logs are local and should avoid secrets; production audit storage needs tamper resistance and retention controls.
- Authorization, review and rollback are mandatory before adding actions affecting files, users, networks or applications.

## Next engineering steps
1. Wire `EdenRuntime` to the native Qt EDEN window with a worker thread (never block GUI).
2. Add an explicit model-selection and local-model-health settings screen.
3. Connect real OS events from authorized, unprivileged sources and test alert fidelity.
4. Build reproducible security datasets and evaluate false positives, missed threats and explanation quality.
5. Add offline speech, OCR/vision and code assistance only after privacy and performance tests.
6. Keep Wazuh and other security tools as optional integrations, not privileged default dependencies.

## Benchmarks
- Offline-only response; startup time; tokens/second; RAM and CPU usage.
- Tool-use accuracy and explicit permission checks.
- Security-event precision/recall and audit reproducibility.
- No unsupported claim of GPT, Claude, Gemini, Defender, Wazuh or CrowdStrike equivalence.
