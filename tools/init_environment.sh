#!/usr/bin/env bash
# Run after the environment has cloned the associated repository.
set -euo pipefail

# Keep the platform-injected proxy, credentials and CA settings intact.
export GIT_TERMINAL_PROMPT=0

# Parse the whole function before reset replaces this script on disk.
initialize_environment() {
    cd /workspace/blocked-sites-in-south-korea
    # Explicitly update origin/work even when the clone only tracks main.
    local fetch_status=0
    timeout 60s git fetch origin +refs/heads/work:refs/remotes/origin/work || fetch_status=$?
    if (( fetch_status != 0 )); then
        if (( fetch_status == 124 )); then
            printf 'Fetching origin/work timed out after 60 seconds.\n' >&2
        else
            printf 'Fetching origin/work failed (exit %s).\n' "$fetch_status" >&2
        fi
        printf 'Check terminal network permission, platform proxy readiness and GitHub access; preserve injected proxy and CA settings.\n' >&2
        return "$fetch_status"
    fi
    git checkout work
    # Intentionally discard tracked local changes to match the remote branch.
    git reset --hard origin/work
    python3 tools/install_workspace_defaults.py
    printf 'Environment initialized at work %s\n' "$(git rev-parse HEAD)"
}

initialize_environment
