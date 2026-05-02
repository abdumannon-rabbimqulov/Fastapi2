import os
import httpx

GEMINI_API_URL = os.getenv("GEMINI_API_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL") or ""


def _extract_text_from_response(data) -> str:
    """Try several common response shapes and return a best-effort text."""
    if data is None:
        return ''
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        # common single-field text
        for k in ("output_text", "text", "content", "reply", "result"):
            v = data.get(k)
            if isinstance(v, str):
                return v
        # Google-style: candidates or outputs
        candidates = data.get('candidates') or data.get('outputs') or data.get('choices')
        if isinstance(candidates, list) and candidates:
            first = candidates[0]
            if isinstance(first, dict):
                for k in ("output", "text", "content", "message"):
                    v = first.get(k)
                    if isinstance(v, str):
                        return v
                # nested content arrays
                for k in ("content",):
                    v = first.get(k)
                    if isinstance(v, list):
                        parts = []
                        for item in v:
                            if isinstance(item, dict) and 'text' in item:
                                parts.append(item['text'])
                        if parts:
                            return "\n".join(parts)
            elif isinstance(first, str):
                return first
        # sometimes result is nested
        if 'response' in data and isinstance(data['response'], dict):
            return _extract_text_from_response(data['response'])
        # fallback
        return str(data)
    # other types
    return str(data)


async def generate_response(prompt: str) -> str:
    """Flexible async adapter for Gemini/Generative endpoints.

    - If GEMINI_API_KEY is set, it's sent as a Bearer header.
    - For Google Generative Language endpoints the GEMINI_API_URL may already
      include the key as a query param; the adapter will still work.
    - The function tries several payload shapes to maximize compatibility.
    """
    if not GEMINI_API_URL:
        raise RuntimeError("GEMINI_API_URL must be set in env")

    headers = {"Content-Type": "application/json"}
    if GEMINI_API_KEY:
        headers["Authorization"] = f"Bearer {GEMINI_API_KEY}"

    # Candidate payloads to try (order matters)
    payloads = []

    # Google Generative API common shapes
    if "generativelanguage.googleapis.com" in (GEMINI_API_URL or ""):
        # chat-like message
        payloads.append({"prompt": {"text": prompt}})
        # simple input
        payloads.append({"input": prompt})
        # instances array style
        payloads.append({"instances": [{"prompt": prompt}]})
    # Generic provider shapes
    payloads.append({"prompt": prompt})
    if GEMINI_MODEL:
        payloads[-1]["model"] = GEMINI_MODEL

    last_exc = None
    async with httpx.AsyncClient(timeout=60.0) as client:
        for payload in payloads:
            try:
                resp = await client.post(GEMINI_API_URL, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                text = _extract_text_from_response(data)
                if text:
                    return text
                # If extraction failed, return raw repr
                return str(data)
            except httpx.HTTPStatusError as e:
                # try next payload on 4xx/5xx
                last_exc = e
                # continue trying other payload formats
                continue
            except Exception as e:
                last_exc = e
                continue

    # If all attempts failed, raise the last exception or a generic error
    if last_exc:
        raise last_exc
    raise RuntimeError("No response from Gemini endpoint")
