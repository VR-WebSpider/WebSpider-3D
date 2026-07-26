REM SPDX-FileCopyrightText: 2026 WebSpider Studios
REM
REM SPDX-License-Identifier: GPL-2.0-or-later

REM First see if there is an environment variable set
if EXIST "%BLENDER_BIN%" (
    goto detect_blender_done
)

REM Check the build folder next, if ninja was used there will be no
REM debug/release folder
set BLENDER_BIN=%BUILD_DIR%\bin\webspider3d.exe
if EXIST "%BLENDER_BIN%" (
    goto detect_blender_done
)

REM Check the release folder next
set BLENDER_BIN=%BUILD_DIR%\bin\release\webspider3d.exe
if EXIST "%BLENDER_BIN%" (
    goto detect_blender_done
)

REM Check the debug folder next
set BLENDER_BIN=%BUILD_DIR%\bin\debug\webspider3d.exe
if EXIST "%BLENDER_BIN%" (
    goto detect_blender_done
)

REM at this point, we don't know where blender is, clear the variable
set BLENDER_BIN=

:detect_blender_done
