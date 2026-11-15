import hashlib
import json
import os
import time
from datetime import datetime, timezone
from typing import List, Dict, Any

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Psique Machine Cognitive Gateway",
    version="0.1.0-mvp",
    description="OpenAI-compatible cognitive middleware & compliance audit proxy by Starcrow Tech"
)

UPSTREAM_BASE_URL = os.getenv("UPSTREAM_BASE_URL", "https://api.openai.com/v1")
LEDGER_FILE = os.getenv("PSIQUE_LEDGER_PATH", "psique_audit_ledger.jsonl")


class ImmutableComplianceLedger:
    """Hash-chained append-only audit ledger for LGPD / ISO 42001 / EU AI Act."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.prev_hash = self._recover_last_hash()

    def _recover_last_hash(self) -> str:
        if not os.path.exists(self.filepath):
            return "0" * 64
        try:
            with open(self.filepath, "rb") as f:
                lines = f.readlines()
                if not lines:
                    return "0" * 64
                last_entry = json.loads(lines[-1].decode("utf-8"))
                return last_entry.get("entry_hash", "0" * 64)
        except Exception:
            return "0" * 64

    def seal_entry(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "prev_hash": self.prev_hash,
            **payload
        }
        serialized = json.dumps(record, sort_keys=True, ensure_ascii=False)
        entry_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        record["entry_hash"] = entry_hash

        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        self.prev_hash = entry_hash
        return record


ledger = ImmutableComplianceLedger(LEDGER_FILE)


def compute_cognitive_overload(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculates Cognitive Overload Index (I_sc) based on guardrail density and history depth."""
    total_chars = sum(len(str(m.get("content", ""))) for m in messages)
    system_chars = sum(
        len(str(m.get("content", "")))
        for m in messages
        if m.get("role") == "system"
    )
    negative_constraints = sum(
        str(m.get("content", "")).lower().count(k)
        for m in messages
        for k in ("never", "do not", "don't", "prohibited", "must not", "não ", "proibido")
    )

    guardrail_ratio = (system_chars / total_chars) if total_chars > 0 else 0.0
    isc_score = min(1.0, round((guardrail_ratio * 0.5) + (negative_constraints * 0.04) + (len(messages) * 0.015), 3))

    return {
        "isc_score": isc_score,
        "status": "OVERLOADED" if isc_score >= 0.65 else "HOMEOSTATIC",
        "negative_constraints_detected": negative_constraints,
        "message_depth": len(messages)
    }


def prune_context(messages: List[Dict[str, Any]], max_turns: int = 10) -> List[Dict[str, Any]]:
    """Decompresses bloated history while preserving system anchors and recent state."""
    if len(messages) <= max_turns:
        return messages
    system_msgs = [m for m in messages if m.get("role") == "system"]
    recent_msgs = [m for m in messages if m.get("role") != "system"][-max_turns:]
    return system_msgs + recent_msgs


@app.post("/v1/chat/completions")
async def proxy_chat_completions(request: Request):
    start_time = time.perf_counter()
    body = await request.json()
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    raw_messages = body.get("messages", [])
    telemetry = compute_cognitive_overload(raw_messages)

    # Trigger semantic decompression if overload threshold is exceeded
    if telemetry["status"] == "OVERLOADED":
        body["messages"] = prune_context(raw_messages)
        intervention = "CONTEXT_PRUNED"
    else:
        intervention = "PASSTHROUGH"

    async with httpx.AsyncClient(timeout=60.0) as client:
        upstream_resp = await client.post(
            f"{UPSTREAM_BASE_URL}/chat/completions",
            headers={"Authorization": auth_header, "Content-Type": "application/json"},
            json=body
        )

    resp_data = upstream_resp.json()
    overhead_ms = round((time.perf_counter() - start_time) * 1000, 2)

    audit_record = ledger.seal_entry({
        "model": body.get("model"),
        "telemetry": telemetry,
        "intervention": intervention,
        "messages_in": len(raw_messages),
        "messages_sent": len(body.get("messages", [])),
        "latency_total_ms": overhead_ms,
        "status_code": upstream_resp.status_code
    })

    headers = {
        "X-Psique-Status": telemetry["status"],
        "X-Psique-ISC": str(telemetry["isc_score"]),
        "X-Psique-Ledger-Hash": audit_record["entry_hash"][:16]
    }
    return JSONResponse(content=resp_data, status_code=upstream_resp.status_code, headers=headers)


@app.get("/health")
def health():
    return {"service": "Psique Machine Gateway", "status": "operational", "ledger_tip": ledger.prev_hash[:16]}
