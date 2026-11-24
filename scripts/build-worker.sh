#!/usr/bin/env bash
# MyStudy v2 — build the Rust worker (WASM + JS entry) via worker-build.
# MUST run from the crate directory: worker-build 0.9.0 resolves its
# staging/output paths relative to the crate root.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../workers/api"
export PATH="$HOME/.cargo/bin:$PATH"

# VM-only workarounds: this VM cannot download from GitHub releases, so
# worker-build's pinned wasm-bindgen CLI and esbuild are supplied from
# local installs when present. On a normal machine these overrides are
# unset and worker-build downloads its own tools.
if [ -z "${WASM_BINDGEN_BIN:-}" ] && [ -x "$HOME/.cargo-wb01/bin/wasm-bindgen" ]; then
  export WASM_BINDGEN_BIN="$HOME/.cargo-wb01/bin/wasm-bindgen"
fi
if [ -z "${ESBUILD_BIN:-}" ]; then
  if command -v esbuild >/dev/null 2>&1; then
    export ESBUILD_BIN="esbuild"
  elif [ -x "$HOME/workspace/wordless/wordless-rust/node_modules/.bin/esbuild" ]; then
    # Read-only reuse of the wordless repo's esbuild; nothing is copied.
    export ESBUILD_BIN="$HOME/workspace/wordless/wordless-rust/node_modules/.bin/esbuild"
  fi
fi

# --no-opt: skip worker-build's own wasm-opt download (blocked in this VM);
# wasm-opt is run below when a binary is available.
worker-build --release --no-opt

WASM_OPT_BIN="${WASM_OPT_BIN:-}"
if [ -z "$WASM_OPT_BIN" ]; then
  for candidate in \
    "$SCRIPT_DIR/../node_modules/.bin/wasm-opt" \
    "$HOME/workspace/wordless/wordless-rust/node_modules/.bin/wasm-opt" \
    "$(command -v wasm-opt || true)"; do
    if [ -n "$candidate" ] && [ -x "$candidate" ]; then
      WASM_OPT_BIN="$candidate"
      break
    fi
  done
fi
WASM_OUT="build/index_bg.wasm"
if [ -n "${MYSTUDY_NO_WASM_OPT:-}" ]; then
  echo "build-worker: MYSTUDY_NO_WASM_OPT=1 — skipping wasm-opt"
elif [ -z "$WASM_OPT_BIN" ]; then
  echo "build-worker: WARNING — wasm-opt not found; WASM is unoptimized." >&2
else
  BEFORE_BYTES="$(stat -c %s "$WASM_OUT")"
  "$WASM_OPT_BIN" \
    --enable-exception-handling --enable-bulk-memory \
    --enable-nontrapping-float-to-int --enable-sign-ext --enable-multivalue \
    --enable-reference-types --enable-simd --enable-tail-call --enable-gc \
    --enable-extended-const \
    --enable-strings --enable-multimemory --enable-mutable-globals \
    --enable-bulk-memory-opt \
    -Oz "$WASM_OUT" -o "$WASM_OUT.opt"
  mv "$WASM_OUT.opt" "$WASM_OUT"
  AFTER_BYTES="$(stat -c %s "$WASM_OUT")"
  echo "build-worker: wasm-opt -Oz: $BEFORE_BYTES -> $AFTER_BYTES bytes (free-tier limit 3145728)"
  if [ "$AFTER_BYTES" -gt 3145728 ]; then
    echo "build-worker: ERROR — optimized WASM still exceeds the free-tier 3 MiB limit." >&2
    exit 1
  fi
fi
