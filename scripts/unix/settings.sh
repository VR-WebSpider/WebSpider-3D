#!/bin/bash
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-2.0-or-later

# WebSpider 3D Application Settings
# Source this file in scripts that need these settings
#
# Configuration priority:
#   1. Environment variables (already set, e.g. from CI or parent shell)
#   2. .env file in repo root (local dev overrides)
#   3. Hardcoded defaults below

# Get the root directory relative to this settings.sh script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Load .env if it exists (local dev overrides)
ENV_FILE="$ROOT_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
fi

# Version always comes from VERSION file (canonical source)
if [ -z "${WEBSPIDER_VERSION:-}" ]; then
    VERSION_FILE="$ROOT_DIR/VERSION"
    if [ -f "$VERSION_FILE" ]; then
        export WEBSPIDER_VERSION="$(cat "$VERSION_FILE" | tr -d '[:space:]')"
    else
        export WEBSPIDER_VERSION="0.0.0"
    fi
fi

# Core environment settings (env var > .env > default)
export WEBSPIDER_ENV="${WEBSPIDER_ENV:-${WEBSPIDER_ENV:-Prod}}"
export WEBSPIDER_BACKEND_URL="${WEBSPIDER_BACKEND_URL:-https://api.webspider3d.com}"
export WEBSPIDER_FRONTEND_URL="${WEBSPIDER_FRONTEND_URL:-https://www.webspider3d.com}"

# App info (constants)
export WEBSPIDER_VERSION_PATCH="${WEBSPIDER_VERSION_PATCH:-0}"
export WEBSPIDER_APP_NAME="${WEBSPIDER_APP_NAME:-WebSpider 3D}"
export WEBSPIDER_EXECUTABLE_NAME="${WEBSPIDER_EXECUTABLE_NAME:-webspider3d}"
export WEBSPIDER_DESCRIPTION="${WEBSPIDER_DESCRIPTION:-WebSpider 3D Content Creation Software}"
export WEBSPIDER_VENDOR="${WEBSPIDER_VENDOR:-WebSpider Studios}"
export WEBSPIDER_WEBSITE="${WEBSPIDER_WEBSITE:-https://webspider3d.com}"

# Bundle settings (constants)
export WEBSPIDER_BUNDLE_IDENTIFIER="${WEBSPIDER_BUNDLE_IDENTIFIER:-com.webspiderstudios.webspider3d}"
export WEBSPIDER_BUNDLE_COPYRIGHT="${WEBSPIDER_BUNDLE_COPYRIGHT:-© 2026 WebSpider Studios}"

# Build settings (constants)
export BLENDER_VERSION="${BLENDER_VERSION:-5.0}"
export PYTHON_VERSION="${PYTHON_VERSION:-3.11}"
export REQUIRED_CMAKE_VERSION="${REQUIRED_CMAKE_VERSION:-3.16}"

# Directory Structure
export BUILD_DIR="${ROOT_DIR}/build"
export SOURCE_DIR="${ROOT_DIR}/source"
export SRC_DIR="${ROOT_DIR}/src"
export CMAKE_DIR="${ROOT_DIR}/cmake"

# Upstream Blender tree (multi-GB, gitignored — populated once per machine).
# Linked git worktrees don't carry ignored files, so a worktree checkout has
# no upstream/ of its own. Resolution order:
#   1. WEBSPIDER_UPSTREAM_DIR (env / .env override)
#   2. this checkout's own upstream/ (a real tree, not an empty dir)
#   3. the main checkout's upstream/ (worktrees share it — overlay.sh only
#      ever READS from $UPSTREAM_DIR, so sharing is safe)
if [ -n "${WEBSPIDER_UPSTREAM_DIR:-${WEBSPIDER_UPSTREAM_DIR:-}}" ]; then
    export UPSTREAM_DIR="${WEBSPIDER_UPSTREAM_DIR:-${WEBSPIDER_UPSTREAM_DIR:-}}"
elif [ -f "${ROOT_DIR}/upstream/CMakeLists.txt" ]; then
    export UPSTREAM_DIR="${ROOT_DIR}/upstream"
else
    _git_common_dir="$(git -C "$ROOT_DIR" rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)"
    _main_checkout_root="${_git_common_dir%/.git}"
    if [ -n "$_git_common_dir" ] && [ -f "${_main_checkout_root}/upstream/CMakeLists.txt" ]; then
        export UPSTREAM_DIR="${_main_checkout_root}/upstream"
        echo "Worktree checkout: sharing upstream from main checkout: $UPSTREAM_DIR" >&2
        # upstream is a submodule pinned per branch — warn (don't fail) when
        # the shared tree isn't at the commit THIS branch pins, so a silent
        # wrong-revision build can't sneak past.
        _pinned="$(git -C "$ROOT_DIR" rev-parse HEAD:upstream 2>/dev/null || true)"
        _actual="$(git -C "$UPSTREAM_DIR" rev-parse HEAD 2>/dev/null || true)"
        if [ -n "$_pinned" ] && [ -n "$_actual" ] && [ "$_pinned" != "$_actual" ]; then
            echo "WARNING: shared upstream is at ${_actual:0:12} but this branch pins ${_pinned:0:12}." >&2
            echo "         Update it (git -C \"$UPSTREAM_DIR\" checkout $_pinned) or set WEBSPIDER_UPSTREAM_DIR." >&2
        fi
        unset _pinned _actual
    else
        # No usable upstream anywhere — keep the default path so the
        # overlay's error message points at the expected location.
        export UPSTREAM_DIR="${ROOT_DIR}/upstream"
    fi
    unset _git_common_dir _main_checkout_root
fi

# Platform-specific settings
if [[ "$OSTYPE" == "darwin"* ]]; then
    export PLATFORM="macOS"
    DEFAULT_CORES=$(sysctl -n hw.ncpu)
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    export PLATFORM="Linux"
    DEFAULT_CORES=$(nproc)
else
    export PLATFORM="Unknown"
    DEFAULT_CORES=4
fi

# Build optimization - define BUILD_CORES before using it
export BUILD_CORES=${BUILD_CORES:-$DEFAULT_CORES}

# Platform-specific build settings (now that BUILD_CORES is defined)
if [[ "$PLATFORM" == "macOS" ]]; then
    # macOS-specific settings
    export CMAKE_GENERATOR_ARGS=""  # Use default (Xcode or Make)
    export BUILD_ARGS="--parallel $BUILD_CORES --config \$CMAKE_BUILD_TYPE"
elif [[ "$PLATFORM" == "Linux" ]]; then
    # Linux-specific settings
    export CMAKE_GENERATOR_ARGS=""  # Use default (Make or Ninja)
    export BUILD_ARGS="--parallel $BUILD_CORES --verbose"
else
    # Generic fallback settings
    export CMAKE_GENERATOR_ARGS=""
    export BUILD_ARGS="--parallel $BUILD_CORES"
fi
