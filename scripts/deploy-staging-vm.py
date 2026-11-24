#!/usr/bin/env python3
"""Deploy MyStudy v2 to Cloudflare staging from this VM.

Gets the scoped Cloudflare API token as an hsurr: surrogate from the
registered custom.cloudflare connection (never prints it) and runs
wrangler with it in the environment. Sentinel/authd swaps the surrogate
for the real token on approved egress to api.cloudflare.com.

Usage:
  python3 scripts/deploy-staging-vm.py [wrangler args...]
Default args: d1 migrations apply, then deploy --env staging.
Set DEPLOY_ONLY=1 to skip migrations, MIGRATE_ONLY=1 to skip deploy.
"""
import os
import subprocess
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import dynamic_credential_entry

ACCOUNT_ID = "b4fc7bb3e29957d6e05fda13b6330adf"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_wrangler(args):
    entry = dynamic_credential_entry("custom.cloudflare")
    surrogate = str(entry["surrogate"]).strip()
    env = dict(os.environ)
    env["CLOUDFLARE_API_TOKEN"] = surrogate
    env["CLOUDFLARE_ACCOUNT_ID"] = ACCOUNT_ID
    env["PATH"] = os.path.expanduser("~/.cargo/bin") + ":" + env.get("PATH", "")
    cmd = ["npx", "wrangler@4"] + args
    print("+ wrangler " + " ".join(args), flush=True)
    result = subprocess.run(cmd, cwd=ROOT, env=env)
    return result.returncode


def main():
    if len(sys.argv) > 1:
        return run_wrangler(sys.argv[1:])
    if not os.environ.get("DEPLOY_ONLY"):
        code = run_wrangler([
            "d1", "migrations", "apply", "mystudy-db-staging",
            "--env", "staging", "--remote",
        ])
        if code != 0:
            return code
    if not os.environ.get("MIGRATE_ONLY"):
        return run_wrangler(["deploy", "--env", "staging"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
