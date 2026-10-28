#!/usr/bin/env bash
# Run after the environment has cloned the associated repository.
set -euo pipefail

# Parse the whole function before reset replaces this script on disk.
initialize_environment() {
    cd /workspace/blocked-sites-in-south-korea
    git fetch origin work
    # Some managed clones do not configure remote-tracking ref updates.
    local fetched_commit
    fetched_commit=$(git rev-parse --verify 'FETCH_HEAD^{commit}')
    git update-ref refs/remotes/origin/work "$fetched_commit"
    git checkout work
    # Intentionally discard tracked local changes to match the remote branch.
    git reset --hard origin/work
    python3 tools/install_workspace_defaults.py
}

initialize_environment
