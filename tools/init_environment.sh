#!/usr/bin/env bash
# Run after the environment has cloned the associated repository.
set -euo pipefail

# Parse the whole function before reset replaces this script on disk.
initialize_environment() {
    cd /workspace/blocked-sites-in-south-korea
    git fetch origin work
    git checkout work
    # Intentionally discard tracked local changes to match the remote branch.
    git reset --hard origin/work
    python3 tools/install_workspace_defaults.py
}

initialize_environment
