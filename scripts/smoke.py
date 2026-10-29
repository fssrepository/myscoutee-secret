#!/usr/bin/env python3
"""Exercise only synthetic data in the local OpenBao development server."""

import json
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:8200"
PATH = "/v1/secret/data/demo/sample"


def request(path, token=None, data=None, method=None):
    headers = {"Accept": "application/json"}
    if token:
        headers["X-Vault-Token"] = token
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode("utf-8")
    req = Request(BASE + path, data=data, headers=headers, method=method)
    with urlopen(req, timeout=5) as response:
        return response.status, response.read()


def main(token_file):
    token = Path(token_file).read_text(encoding="utf-8").strip()
    if not token:
        raise RuntimeError("The sandbox token file is empty")

    status, _ = request("/v1/sys/health")
    assert status == 200, "OpenBao is not unsealed and healthy"
    status, page = request("/ui/")
    assert status == 200 and b"html" in page.lower(), "The web UI is unavailable"

    payload = {"data": {"example": "sandbox-only-value"}}
    status, _ = request(PATH, token=token, data=payload, method="POST")
    assert status == 200, "The synthetic KV write failed"
    status, body = request(PATH, token=token)
    value = json.loads(body)["data"]["data"]["example"]
    assert status == 200 and value == payload["data"]["example"], "KV read mismatch"

    try:
        request(PATH, token="invalid-sandbox-token")
    except HTTPError as error:
        assert error.code == 403, "Expected access denial for an invalid token"
    else:
        raise AssertionError("Invalid token unexpectedly read the synthetic value")

    print("PASS: health, web UI, synthetic KV write/read, invalid-token denial")
    print("UI sample: Secrets > secret > demo > sample")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: smoke.py TOKEN_FILE")
    main(sys.argv[1])
