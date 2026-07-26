REM SPDX-FileCopyrightText: 2026 WebSpider Studios
REM
REM SPDX-License-Identifier: GPL-2.0-or-later

@echo off
setlocal enabledelayedexpansion

REM WebSpider 3D Install Script for Windows
REM Installs scripts using CMake

REM Load all settings from settings.bat
set "SCRIPT_DIR=%~dp0"
call "%SCRIPT_DIR%settings.bat"

REM Use WEBSPIDER_ENV directly from settings.bat (loaded from webspider.json)
REM Define build directory for this environment
if "%WEBSPIDER_ENV%"=="" (
    echo Warning: WEBSPIDER_ENV is empty, using fallback Prod
    set "WEBSPIDER_ENV=Prod"
)
set "BUILD_ENV_DIR=%BUILD_DIR%\%WEBSPIDER_ENV%"
set "BLENDER_BUILD_ENV=Release"

echo Clearing previous source directory...
cd /d "%ROOT_DIR%"
if exist "%SOURCE_DIR%\scripts" rmdir /s /q "%SOURCE_DIR%\scripts"
mkdir "%SOURCE_DIR%\scripts"

robocopy "%UPSTREAM_DIR%\scripts" "%SOURCE_DIR%\scripts" /E /COPY:DAT
if !ERRORLEVEL! GEQ 8 (
    echo Error: Failed to copy upstream scripts
    exit /b 1
)

echo Overlaying WebSpider 3D scripts onto source...
robocopy "%SRC_DIR%\scripts" "%SOURCE_DIR%\scripts" /E /COPY:DAT
if !ERRORLEVEL! GEQ 8 (
    echo Error: Failed to overlay WebSpider 3D scripts
    exit /b 1
)

REM Reset ERRORLEVEL before cmake
cmd /c "exit /b 0"

echo Installing scripts using CMake...
if defined BUILD_WITH_NINJA (
    cmake --build "%BUILD_ENV_DIR%" --target install
) else (
    cmake --build "%BUILD_ENV_DIR%" --target install --config "%BLENDER_BUILD_ENV%"
)

if !ERRORLEVEL! neq 0 (
    echo Error: Scripts install failed
    exit /b 1
)

echo Scripts installation complete.
echo Run WebSpider 3D using: %BUILD_ENV_DIR%\bin\%BLENDER_BUILD_ENV%\webspider3d.exe
exit /b 0
