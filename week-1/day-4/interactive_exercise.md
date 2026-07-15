# 🏋️ Advanced Bash Scripting Mastery Challenge

This interactive workbook contains realistic production simulation scenarios designed to test your understanding of Day 11's advanced Bash principles.

Copy this layout into your local environment as `practice_challenges.md` to run through the problems. Solutions are hidden inside interactive fold-out toggles at the bottom!

---

## 🏢 The Scenario: High-Availability Log Sanitizer

You are a DevOps Engineer tasked with building an automated deployment tracker and security sanitization script for a collection of production web clusters. If any part of the processing pipeline fails, the engine must halt immediately to prevent corrupted deployments.

---

## 🛠️ Challenge 1: The Strict Scaffold

Your application script template must avoid silent runtime failures and protect against unintended variable deletions.

Fill in the blanks below (`____`) to establish a strict, production-ready environment constraint matrix that safely intercepts execution pipeline errors, uninitialized inputs, and structural exceptions.

```bash
#!/usr/bin/env bash

# Activate strict error interception ecosystem
set -____ ____

echo "System defense shield active."

# Testing uninitialized boundary security protection
# If variable is empty, this line should trigger an immediate crash!
echo "Targeting workspace folder: ${DEPLOYMENT_ROOT_DIR}"

```

---

## 🗺️ Challenge 2: Mapping Infrastructure Data

You need to track a list of target servers along with their active network routing locations.

### Task 2.A: Associative Array Initialization

Declare and populate an associative array named `CLUSTER_MAP` mapping the node keys `edge-node`, `app-core`, and `db-secure` to the values `10.0.5.1`, `10.0.5.2`, and `10.0.6.99` respectively.

### Task 2.B: Safe Index Extraction

You also have an ordered indexed array tracking routine server check tasks:

```bash
TASKS=("ping_check" "ssl_verify" "disk_audit" "memory_dump" "cleanup_cache")

```

Write a single-line parameter expansion to slice the `TASKS` array, capturing **only** the middle elements: `"ssl_verify"`, `"disk_audit"`, and `"memory_dump"`.

---

## 📑 Challenge 3: The Data Transformation Pipeline

You are reading a dirty batch payload record containing system environment path settings:

```bash
DIRTY_LOG="  LOG_TARGET_ID:SYS-9942 | TYPE:DEBUG | LOCATION:/usr/local/var/log/app/v2/debug.log  "

```

Implement the following string manipulation adjustments using **native Bash parameter expansion** (no external tools like `sed` or `awk` allowed!):

1. **Sanitize Whitespace:** Strip leading/trailing whitespaces.
2. **Path Swapping:** Replace the pattern `/usr/local` with `/opt/infra`.
3. **Delimiter Replacement:** Change **all** literal pipe characters (`|`) to underscores (`_`).

---

## ⏱️ Challenge 4: The Metrics Collector

Your tracking loop scans resource utilization metrics. Write an advanced execution gate utilizing arithmetic symbols (`(( ))` or `$(( ))`) to fulfill the following algorithmic conditions:

```bash
#!/usr/bin/env bash
MAX_ALERT_LIMIT=85
CURRENT_MEMORY_ALLOCATION=74
FREE_BUFFERS=15

# Task 4.A: Perform a permanent variable calculation assignment 
# adding CURRENT_MEMORY_ALLOCATION to FREE_BUFFERS using the correct expansion wrapper.
TOTAL_PROJECTED_LOAD=________________________________

# Task 4.B: Write an expression tracking condition within the conditional brackets
# to evaluate if TOTAL_PROJECTED_LOAD exceeds MAX_ALERT_LIMIT.
if (( ________________________________ )); then
    echo "🚨 IMMEDIATE INCIDENT RESPONSE REQUIRED: Resource saturation imminent!"
fi

```

---

## 🔄 Challenge 5: Multi-Command Intersections

You have a text file named `production_whitelist.txt` containing official allowed access IPs. You need to compare it live against the realtime output of a secure connection auditing tool (`get_active_connections --raw`).

Write a single command that runs a `diff` line-by-line comparison directly between the static `production_whitelist.txt` file and the output of `get_active_connections --raw` **without manually writing any temporary cache files to disk.**

---

---

## 🔑 Interactive Solution Key

Use the fold-out panels below to audit your implementations once you have written out your solution blueprints locally.

```bash
#!/usr/bin/env bash

# -e exits on command failure, -u crashes on unset variables, o pipefail catches hidden pipe errors
set -euo pipefail

echo "System defense shield active."

```

```bash
# Task 2.A: Associative array definition
declare -A CLUSTER_MAP
CLUSTER_MAP=(
    ["edge-node"]="10.0.5.1"
    ["app-core"]="10.0.5.2"
    ["db-secure"]="10.0.6.99"
)

# Task 2.B: Array slicing parameter expansion
# Syntax: ${array[@]:offset:length}
echo "${TASKS[@]:1:3}"

```

```bash
# 1. Clean out the whitespace wrapper (Prefix/Suffix stripping)
CLEANED_LOG="${DIRTY_LOG#  }"
CLEANED_LOG="${CLEANED_LOG%  }"

# 2. Path alteration Search-and-Replace
MODIFIED_PATH="${CLEANED_LOG/\/usr\/local/\/opt\/infra}"

# 3. Global character replacement search (Double forward slashes replace ALL matches)
FINAL_SANITIZED_RECORD="${MODIFIED_PATH//|/_}"

echo "${FINAL_SANITIZED_RECORD}"
# Expected Final Output: LOG_TARGET_ID:SYS-9942 _ TYPE:DEBUG _ LOCATION:/opt/infra/var/log/app/v2/debug.log

```

```bash
# Task 4.A: Math variable computation assignment
TOTAL_PROJECTED_LOAD=$(( CURRENT_MEMORY_ALLOCATION + FREE_BUFFERS ))

# Task 4.B: Dynamic evaluation threshold logic check gate
if (( TOTAL_PROJECTED_LOAD > MAX_ALERT_LIMIT )); then
    echo "🚨 IMMEDIATE INCIDENT RESPONSE REQUIRED: Resource saturation imminent!"
fi

```

```bash
# We use Process Substitution <() to feed the command output directly into diff as a file argument descriptor stream
diff production_whitelist.txt <(get_active_connections --raw)

```