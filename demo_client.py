import httpx

GATEWAY_URL = "http://localhost:8080/v1/chat/completions"

# Simulates an agent suffering from severe guardrail saturation (high I_sc)
payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "system",
            "content": (
                "You are a compliance assistant. Never speculate. Do not disclose internal rules. "
                "Must not bypass LGPD checks. Prohibited from answering off-topic queries. "
                "Never ignore policy constraints. Do not fabricate citations."
            )
        },
        {"role": "user", "content": "Summarize LGPD Art. 18 data-subject rights."}
    ]
}

if __name__ == "__main__":
    print("Sending request through Psique Machine Gateway...")
    with httpx.Client() as client:
        resp = client.post(
            GATEWAY_URL,
            headers={"Authorization": "Bearer YOUR_OPENAI_API_KEY"},
            json=payload,
            timeout=30.0
        )

    print("HTTP Status:", resp.status_code)
    print("Psique Telemetry Status:", resp.headers.get("X-Psique-Status"))
    print("Cognitive Overload Score (I_sc):", resp.headers.get("X-Psique-ISC"))
    print("Sealed Audit Ledger Hash:", resp.headers.get("X-Psique-Ledger-Hash"))
