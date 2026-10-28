#!/usr/bin/env bash
# Run after the environment has cloned the associated repository.
set -euo pipefail

cd /workspace/blocked-sites-in-south-korea
git checkout work
python3 tools/install_workspace_defaults.py
