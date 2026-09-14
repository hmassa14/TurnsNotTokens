#!/bin/bash
# Swapped-in replacement for Spotify's lib/aika.sh.
#
# Upstream sends the message to a Portal AiKA "mode" (a hosted Gemini 2.5 Flash agent) via
# `portal-cli actions aika:invoke-chat`. That service is internal to Spotify. This file keeps the
# same function contract (shunt_preflight, shunt_tmpfile, shunt_invoke) and routes the message to a
# cheap model with the mode's instructions from the upstream README as the system prompt.
#
# Transport, in order of preference:
#   1. ANTHROPIC_API_KEY set  -> one Messages API call (curl). No tools, no Claude Code system prompt,
#      temperature 0.2 as upstream sets. This is the faithful stand-in for a Portal call.
#   2. otherwise              -> one-turn headless Claude Code call with --tools "" so no tool
#      definitions enter the worker's prompt. Needed when the only auth is a Claude subscription.
#      Temperature cannot be set on this path.
# Either way every call's JSON (usage, cost, duration, transport) is saved under $SHUNT_RUN_DIR/worker
# so the harness counts the worker's tokens and cost.

SHUNT_TIMEOUT_SECONDS="${SHUNT_TIMEOUT_SECONDS:-180}"
SHUNT_WORKER_MODEL="${SHUNT_WORKER_MODEL:-claude-haiku-4-5}"
SHUNT_WORKER_MAX_TOKENS="${SHUNT_WORKER_MAX_TOKENS:-8192}"
SHUNT_WORKER_TEMPERATURE="${SHUNT_WORKER_TEMPERATURE:-0.2}"
# Haiku 4.5 list price per million tokens: input, cache write (5m), cache read, output.
SHUNT_WORKER_PRICES="${SHUNT_WORKER_PRICES:-1.0,1.25,0.1,5.0}"

BULK_READER_INSTRUCTIONS='You are a precise code analyst. Read the provided files and answer the question concisely. Output structured bullets only. No greetings, no prose, no preambles, no summaries. Lead every bullet with the exact name, type, or line number. Use nested bullets for details. Skip anything the caller did not ask for.'
CODE_WRITER_INSTRUCTIONS='You generate code files based on a spec and reference files. Match the existing patterns, conventions, naming, and style exactly. Output only the code — no explanations, no markdown fences unless asked. If the spec is ambiguous, make reasonable choices that match the patterns in the reference code.'

SHUNT_TMPFILES=()
shunt_tmpfile() {
  local f
  f=$(mktemp) || return 1
  SHUNT_TMPFILES+=("$f")
  trap 'rm -f "${SHUNT_TMPFILES[@]}"' EXIT
  printf -v "$1" '%s' "$f"
}

shunt_preflight() {
  local missing=""
  command -v jq >/dev/null 2>&1 || missing=" jq"
  if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    command -v curl >/dev/null 2>&1 || missing="$missing curl"
  else
    command -v claude >/dev/null 2>&1 || missing="$missing claude"
  fi
  if [ -n "$missing" ]; then
    echo "Error: missing required command(s):$missing" >&2
    return 1
  fi
  return 0
}

# One Messages API call. Writes a JSON record shaped like Claude Code's -p output
# (result, usage, total_cost_usd, duration_ms) plus transport and model, so the harness reads both alike.
_shunt_invoke_api() {
  local instructions="$1" message_file="$2" out_file="$3"
  local base url body raw t0 t1 http
  base="${ANTHROPIC_BASE_URL:-https://api.anthropic.com}"
  url="${base%/}/v1/messages"
  body=$(jq -n --arg model "$SHUNT_WORKER_MODEL" --arg sys "$instructions" --rawfile msg "$message_file" \
           --argjson max "$SHUNT_WORKER_MAX_TOKENS" --argjson temp "$SHUNT_WORKER_TEMPERATURE" \
           '{model:$model, max_tokens:$max, temperature:$temp, system:$sys, messages:[{role:"user", content:$msg}]}')
  t0=$(date +%s%3N)
  raw=$(curl -sS --max-time "$SHUNT_TIMEOUT_SECONDS" -w '\n%{http_code}' "$url" \
          -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" \
          --data-binary "$body") || return 1
  t1=$(date +%s%3N)
  http="${raw##*$'\n'}"; raw="${raw%$'\n'*}"
  if [ "$http" != "200" ]; then
    echo "Error: worker API returned HTTP $http: $(printf '%s' "$raw" | head -c 400)" >&2
    return 1
  fi
  printf '%s' "$raw" | jq --arg prices "$SHUNT_WORKER_PRICES" --argjson ms "$((t1 - t0))" '
    ($prices | split(",") | map(tonumber)) as $p
    | .usage as $u
    | {
        transport: "api", model: .model, duration_ms: $ms,
        result: ([.content[] | select(.type=="text") | .text] | join("")),
        usage: {
          input_tokens: ($u.input_tokens // 0),
          cache_creation_input_tokens: ($u.cache_creation_input_tokens // 0),
          cache_read_input_tokens: ($u.cache_read_input_tokens // 0),
          output_tokens: ($u.output_tokens // 0)
        },
        total_cost_usd: ((($u.input_tokens // 0) * $p[0] + ($u.cache_creation_input_tokens // 0) * $p[1]
                          + ($u.cache_read_input_tokens // 0) * $p[2] + ($u.output_tokens // 0) * $p[3]) / 1000000),
        stop_reason: .stop_reason
      }' > "$out_file"
}

# One-turn headless Claude Code call with no tools. Fallback when there is no API key.
_shunt_invoke_cli() {
  local instructions="$1" message_file="$2" out_file="$3" stderr_file="$4" run_id="$5"
  env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT \
    OTEL_RESOURCE_ATTRIBUTES="run.id=${run_id}__worker" \
    CLAUDE_CODE_PROMPT_CACHE_TTL="${CLAUDE_CODE_PROMPT_CACHE_TTL:-5m}" \
    timeout "$SHUNT_TIMEOUT_SECONDS" \
    claude -p --model "$SHUNT_WORKER_MODEL" --system-prompt "$instructions" --tools "" \
      --max-turns 1 --output-format json \
      < "$message_file" > "$out_file" 2>"$stderr_file" || return 1
  # annotate transport in place
  jq --arg m "$SHUNT_WORKER_MODEL" '. + {transport: "cli", model: (.model // $m)}' "$out_file" > "$out_file.tmp" && mv "$out_file.tmp" "$out_file"
}

# $1 mode name, $2 file holding the message. Prints the worker's answer.
shunt_invoke() {
  local mode_name="$1" message_file="$2"
  local instructions out_dir stamp out_file stderr_file rc text run_id
  case "$mode_name" in
    bulk-reader) instructions="$BULK_READER_INSTRUCTIONS" ;;
    code-writer) instructions="$CODE_WRITER_INSTRUCTIONS" ;;
    *) echo "Error: unknown mode $mode_name" >&2; return 1 ;;
  esac
  out_dir="${SHUNT_RUN_DIR:-/tmp/shunt}/worker"
  mkdir -p "$out_dir"
  run_id=$(basename "${SHUNT_RUN_DIR:-shunt}")
  stamp=$(date +%s%N)
  out_file="$out_dir/${stamp}-${mode_name}.json"
  stderr_file=$(mktemp)
  if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    _shunt_invoke_api "$instructions" "$message_file" "$out_file" 2>"$stderr_file"; rc=$?
  else
    _shunt_invoke_cli "$instructions" "$message_file" "$out_file" "$stderr_file" "$run_id"; rc=$?
  fi
  if [ "$rc" -ne 0 ]; then
    echo "Error: worker call failed (exit $rc)" >&2
    cat "$stderr_file" >&2; rm -f "$stderr_file"
    return 1
  fi
  rm -f "$stderr_file"
  text=$(jq -r '.result // empty' "$out_file" 2>/dev/null)
  if [ -z "$text" ]; then
    echo "Error: worker returned no text" >&2
    return 1
  fi
  printf '%s\n' "$text"
}
