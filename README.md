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
