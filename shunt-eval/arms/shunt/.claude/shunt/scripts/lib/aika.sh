#!/bin/bash
# Swapped-in replacement for Spotify's lib/aika.sh.
#
# Upstream sends the message to a Portal AiKA "mode" (a hosted Gemini 2.5 Flash agent) via
# `portal-cli actions aika:invoke-chat`. That service is internal to Spotify. This file keeps the
# same function contract (shunt_preflight, shunt_tmpfile, shunt_invoke) and routes the message to
# a one-turn headless Claude Code call on Haiku, with the mode's instructions from the upstream
# README as the system prompt. Every call's JSON output is saved under $SHUNT_RUN_DIR/worker so the
# worker's tokens and cost are counted by the evaluation harness.

SHUNT_TIMEOUT_SECONDS="${SHUNT_TIMEOUT_SECONDS:-180}"
SHUNT_WORKER_MODEL="${SHUNT_WORKER_MODEL:-claude-haiku-4-5}"

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
  command -v claude >/dev/null 2>&1 || missing="$missing claude"
  if [ -n "$missing" ]; then
    echo "Error: missing required command(s):$missing" >&2
    return 1
  fi
  return 0
}

# $1 mode name, $2 file holding the message. Prints the worker's answer.
shunt_invoke() {
  local mode_name="$1" message_file="$2"
  local instructions out_dir stamp out_file stderr_file rc text run_id workdir
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
  # Run from an empty directory so the worker does not load this workspace's hooks and skills.
  workdir=$(mktemp -d)
  env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT \
    OTEL_RESOURCE_ATTRIBUTES="run.id=${run_id}__worker" \
    timeout "$SHUNT_TIMEOUT_SECONDS" \
    claude -p --model "$SHUNT_WORKER_MODEL" --system-prompt "$instructions" \
      --max-turns 1 --output-format json \
      < "$message_file" > "$out_file" 2>"$stderr_file"
  rc=$?
  rmdir "$workdir" 2>/dev/null
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
