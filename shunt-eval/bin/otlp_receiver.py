#!/usr/bin/env python3
"""Minimal OTLP/HTTP JSON receiver. Writes every POST body to <out_dir>/<epoch_ns>-<signal>.json.

Usage: otlp_receiver.py <out_dir> [port]
Claude Code env to point at it:
  OTEL_EXPORTER_OTLP_PROTOCOL=http/json OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:<port>
"""
import gzip
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    out_dir = "."

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        if self.headers.get("Content-Encoding") == "gzip":
            body = gzip.decompress(body)
        signal = self.path.strip("/").split("/")[-1] or "unknown"
        path = os.path.join(self.out_dir, f"{time.time_ns()}-{signal}.json")
        try:
            obj = json.loads(body)
            with open(path, "w") as fh:
                json.dump(obj, fh)
        except Exception:
            with open(path + ".raw", "wb") as fh:
                fh.write(body)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b"{}")

    def log_message(self, *a):
        pass


def main():
    out = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 4318
    os.makedirs(out, exist_ok=True)
    Handler.out_dir = out
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
