    # Psique Machine Gateway (`@cognitive-proxy-1`)

**Cognitive Middleware & OpenAI-Compatible AI Governance Proxy by Starcrow Tech**

Psique Machine intercepts LLM API traffic between autonomous agents (LangGraph, AutoGen, CrewAI, MCP, Fetch.ai A2A) and model providers—reducing token costs by up to **60%**, eliminating **guardrail friction & cognitive overload**, and sealing every decision into an **immutable, hash-chained audit ledger** aligned with **LGPD**, **ISO/IEC 42001**, and the **EU AI Act**.

---

## Architecture Overview

```text
[ Autonomous Agents / Front-end ]
               │
               ▼  (Drop-in OpenAI-compatible base_url)
┌─────────────────────────────────────────────────────────────┐
│               PSIQUE MACHINE MIDDLEWARE CORE                │
│                                                             │
│  1. Entropy & Friction Sensor  ──► Cognitive Overload (Isc) │
│  2. Semantic Context Pruner    ──► -40% to -60% Token Cost  │
│  3. Attractor State Kernel     ──► Stable Agent Identity    │
│  4. Immutable Audit Wrapper    ──► Hash-Chained WORM Logs   │
└─────────────────────────────────────────────────────────────┘
               │
               ▼
[ OpenAI / Anthropic / Gemini / Local Sub-Kernels ]
```

---

## Quickstart (In-VPC / Local Deployment)

### Option 1: Run with Docker (Recommended)
```bash
git clone [https://github.com/ferreirajacicley7-cpu/psique-machine-gateway.git](https://github.com/ferreirajacicley7-cpu/psique-machine-gateway.git)
cd psique-machine-gateway
docker build -t psique-gateway .
docker run -p 8080:8080 -e UPSTREAM_BASE_URL="[https://api.openai.com/v1](https://api.openai.com/v1)" psique-gateway
```

### Option 2: Run with Python / Uvicorn
```bash
pip install -r requirements.txt
uvicorn gateway:app --host 0.0.0.0 --port 8080
```

---

## Zero-Rewrite Integration

Point any OpenAI-compatible SDK to your Psique Machine gateway instance:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",  # Psique Machine Gateway
    api_key="your-upstream-provider-key"
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Analyze portfolio risk under LGPD rules."}]
)
```

---

## Core Capabilities

* **Cognitive Overload Telemetry (`I_sc`):** Detects guardrail saturation, circular reasoning loops, and context pollution before latency spikes or hallucinations reach end users.
* **Semantic Context Pruning:** Compresses redundant system prompts and noisy conversation history without altering agent intent.
* **Compliance-by-Design Ledger:** Generates tamper-evident JSON records (`entry_hash` + `prev_hash`) ready for **LGPD**, **ISO/IEC 42001**, and **EU AI Act** audits.

---

## Enterprise Onboarding & 30-Day Paid POC

Starcrow Tech offers a **30-day In-VPC Paid Proof of Concept (POC)** with a contractual performance guarantee (≥30% token reduction at equal or better quality).

* **Live Agent on Fetch.ai / ASI:One:** [`@cognitive-proxy-1`](https://asi1.ai/ai/cognitive-proxy-1)
* **Architecture & Live Telemetry Demo:** [Psique Machine Artifact](https://asi1.ai/artifact/57eb5f45-dd6d-445a-b0a2-7fc3cd7c6bd8)
* **Technical Contact:** `poc@starcrow.tech`
