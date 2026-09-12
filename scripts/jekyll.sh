#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Prefer Homebrew Ruby over macOS's obsolete system Ruby, when available.
if [ -x /opt/homebrew/opt/ruby/bin/ruby ]; then
  export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
fi
export BUNDLE_PATH="${BUNDLE_PATH:-vendor/bundle}"
exec bundle exec jekyll "$@"
