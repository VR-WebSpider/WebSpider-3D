REM SPDX-FileCopyrightText: 2026 WebSpider Studios
REM
REM SPDX-License-Identifier: GPL-2.0-or-later

@echo off
REM WebSpider 3D Application Settings for Windows
REM Source this file in batch scripts that need these settings
REM
REM Configuration priority:
REM   1. Environment variables (already set, e.g. from CI)
REM   2. .env file in repo root (local dev overrides)
REM   3. Hardcoded defaults below

REM Get the root directory relative to this settings.bat script
for %%i in ("%~dp0..\..") do set "ROOT_DIR=%%~fi"

REM Load .env if it exists (local dev overrides)
if exist "%ROOT_DIR%\.env" (
    for /f "usebackq eol=# tokens=1,* delims==" %%a in ("%ROOT_DIR%\.env") do (
        if not "%%a"=="" if not "%%b"=="" (
            REM Only set if not already defined (env vars take priority)
            if not defined %%a set "%%a=%%b"
        )
    )
)

REM Version always comes from VERSION file (canonical source)
if not defined WEBSPIDER_VERSION (
    if defined WEBSPIDER_VERSION (
        set "WEBSPIDER_VERSION=%WEBSPIDER_VERSION%"
    ) else if exist "%ROOT_DIR%\VERSION" (
        set /p WEBSPIDER_VERSION=<"%ROOT_DIR%\VERSION"
    ) else (
        set "WEBSPIDER_VERSION=0.0.0"
    )
)

REM Core environment settings (env var > .env > default)
if not defined WEBSPIDER_ENV (
    if defined WEBSPIDER_ENV (
        set "WEBSPIDER_ENV=%WEBSPIDER_ENV%"
    ) else (
        set "WEBSPIDER_ENV=Prod"
    )
)
if not defined WEBSPIDER_BACKEND_URL set "WEBSPIDER_BACKEND_URL=https://api.webspider3d.com"
if not defined WEBSPIDER_FRONTEND_URL set "WEBSPIDER_FRONTEND_URL=https://www.webspider3d.com"

REM App info (constants)
if not defined WEBSPIDER_VERSION_PATCH set "WEBSPIDER_VERSION_PATCH=0"
if not defined WEBSPIDER_APP_NAME set "WEBSPIDER_APP_NAME=WebSpider 3D"
if not defined WEBSPIDER_EXECUTABLE_NAME set "WEBSPIDER_EXECUTABLE_NAME=webspider3d"
if not defined WEBSPIDER_DESCRIPTION set "WEBSPIDER_DESCRIPTION=WebSpider 3D Content Creation Software"
if not defined WEBSPIDER_VENDOR set "WEBSPIDER_VENDOR=WebSpider Studios"
if not defined WEBSPIDER_WEBSITE set "WEBSPIDER_WEBSITE=https://webspider3d.com"

REM Bundle settings (constants)
if not defined WEBSPIDER_BUNDLE_IDENTIFIER set "WEBSPIDER_BUNDLE_IDENTIFIER=com.webspiderstudios.webspider3d"
if not defined WEBSPIDER_BUNDLE_COPYRIGHT set "WEBSPIDER_BUNDLE_COPYRIGHT=© 2026 WebSpider Studios"

REM Build settings (constants)
if not defined BLENDER_VERSION set "BLENDER_VERSION=5.0"
if not defined PYTHON_VERSION set "PYTHON_VERSION=3.11"
if not defined REQUIRED_CMAKE_VERSION set "REQUIRED_CMAKE_VERSION=3.16"

REM Windows-specific build settings
set "BLENDER_BUILD_TYPE=Release"

REM Directory Structure
set "BUILD_DIR=%ROOT_DIR%\build"
set "SOURCE_DIR=%ROOT_DIR%\source"
set "SRC_DIR=%ROOT_DIR%\src"
set "CMAKE_DIR=%ROOT_DIR%\cmake"

REM Upstream Blender tree (multi-GB, gitignored). Linked git worktrees don't
REM carry ignored files, so fall back to the main checkout's upstream\ (the
REM overlay only reads from it). Mirrors scripts/unix/settings.sh.
if defined WEBSPIDER_UPSTREAM_DIR (
    set "UPSTREAM_DIR=%WEBSPIDER_UPSTREAM_DIR%"
) else if defined WEBSPIDER_UPSTREAM_DIR (
    set "UPSTREAM_DIR=%WEBSPIDER_UPSTREAM_DIR%"
) else (
    set "UPSTREAM_DIR=%ROOT_DIR%\upstream"
    if not exist "%ROOT_DIR%\upstream\CMakeLists.txt" (
        for /f "usebackq delims=" %%g in (`git -C "%ROOT_DIR%" rev-parse --path-format=absolute --git-common-dir 2^>nul`) do (
            for %%m in ("%%g\..") do (
                if exist "%%~fm\upstream\CMakeLists.txt" (
                    set "UPSTREAM_DIR=%%~fm\upstream"
                    echo Worktree checkout: sharing upstream from main checkout: %%~fm\upstream 1>&2
                )
            )
        )
    )
)

REM Platform-specific settings
set "PLATFORM=Windows"

REM Get number of CPU cores (Windows) - Reserve 2 cores for system
set /a "DEFAULT_CORES=%NUMBER_OF_PROCESSORS%-2"
if %DEFAULT_CORES% LEQ 2 set "DEFAULT_CORES=2"

REM Build optimization - Use BUILD_CORES if set, otherwise use DEFAULT_CORES
if not defined BUILD_CORES (
    set "BUILD_CORES=%DEFAULT_CORES%"
) else (
    echo Using custom BUILD_CORES: %BUILD_CORES%
)

REM Windows-specific build settings - Select generator based on BUILD_WITH_NINJA
if defined BUILD_WITH_NINJA (
    set "CMAKE_GENERATOR_ARGS=-G Ninja"
    set "BUILD_ARGS=--parallel %BUILD_CORES%"
) else (
    REM Use Visual Studio generator - multi-config, creates Debug/Release folders
    set "CMAKE_GENERATOR_ARGS=-G "Visual Studio 17 2022" -A x64"
    set "BUILD_ARGS=--parallel %BUILD_CORES% --verbose -- /m:%BUILD_CORES%"
)

exit /b 0
