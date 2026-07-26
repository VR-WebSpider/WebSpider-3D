REM SPDX-FileCopyrightText: 2026 WebSpider Studios
REM
REM SPDX-License-Identifier: GPL-2.0-or-later

@echo off
REM WebSpider 3D Build Script - MSBuild (forced)
REM Forces Visual Studio MSBuild generator regardless of detection, then delegates to build.bat.
set "BUILD_WITH_NINJA=0"
call "%~dp0build.bat"
exit /b %ERRORLEVEL%
