#!/usr/bin/env python3
"""Call DeepSeek with DEEPSEEK_API_KEY using only the Python standard library."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

URL = "https://api.deepseek.com/chat/completions"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?", help="Omit to read from stdin")
    parser.add_argument("--model", default="deepseek-flash")
    parser.add_argument("--allow-other-model", action="store_true",
                        help="Allow a non-Flash model only with explicit user authorization")
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--check", action="store_true", help="Check key presence without an API request")
    args = parser.parse_args()
    if args.model != "deepseek-flash" and not args.allow_other_model:
        parser.error("Only deepseek-flash is allowed by default. Other models require explicit user authorization and --allow-other-model.")
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("Missing DEEPSEEK_API_KEY. Add it through environment Secrets.", file=sys.stderr)
        return 2
    if args.check:
        print("DEEPSEEK_API_KEY is configured; API connectivity and key validity are unverified.")
        return 0
    if args.max_tokens <= 0 or not 0 < args.timeout < float("inf"):
        parser.error("--max-tokens must be positive and --timeout must be positive and finite")
    if args.prompt is None and sys.stdin.isatty():
        parser.error("Provide a prompt or pipe text to stdin")
    prompt = args.prompt if args.prompt is not None else sys.stdin.read()
    if not prompt.strip():
        parser.error("Prompt cannot be empty")
    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": args.max_tokens,
        "stream": False,
    }
    request = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        # Inherit proxy and CA settings; refuse redirects carrying credentials.
        with urllib.request.build_opener(NoRedirect).open(request, timeout=args.timeout) as response:
            result = json.load(response)
        content = result["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise ValueError("Missing text response")
        print(content)
        return 0
    except urllib.error.HTTPError as error:
        # Response bodies and headers may contain sensitive information.
        print(f"DeepSeek HTTP {error.code}: check network policy, credentials, balance and model access.", file=sys.stderr)
    except (urllib.error.URLError, TimeoutError, OSError):
        print("DeepSeek connection failed: check network policy, proxy and timeout.", file=sys.stderr)
    except (ValueError, KeyError, IndexError, TypeError):
        print("DeepSeek returned an unexpected response format.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
