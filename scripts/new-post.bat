@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
set /p TITLE="Post title: "
set /p CATEGORY="Category (AI/Development/Knowledge/Project): "

:: Extract year and month
for /f "tokens=1-3 delims=-" %%a in ('date /t') do (
    set YEAR=%%a
    set MONTH=%%b
)

:: Create slug for folder name
set SLUG=%TITLE%

:: Remove leading and trailing spaces
:strip_start
if "!SLUG:~0,1!"==" " (
    set SLUG=!SLUG:~1!
    goto strip_start
)
:strip_end
if "!SLUG:~-1!"==" " (
    set SLUG=!SLUG:~0,-1!
    goto strip_end
)

:: Convert to lowercase (simple and reliable)
set SLUG=!SLUG:A=a!
set SLUG=!SLUG:B=b!
set SLUG=!SLUG:C=c!
set SLUG=!SLUG:D=d!
set SLUG=!SLUG:E=e!
set SLUG=!SLUG:F=f!
set SLUG=!SLUG:G=g!
set SLUG=!SLUG:H=h!
set SLUG=!SLUG:I=i!
set SLUG=!SLUG:J=j!
set SLUG=!SLUG:K=k!
set SLUG=!SLUG:L=l!
set SLUG=!SLUG:M=m!
set SLUG=!SLUG:N=n!
set SLUG=!SLUG:O=o!
set SLUG=!SLUG:P=p!
set SLUG=!SLUG:Q=q!
set SLUG=!SLUG:R=r!
set SLUG=!SLUG:S=s!
set SLUG=!SLUG:T=t!
set SLUG=!SLUG:U=u!
set SLUG=!SLUG:V=v!
set SLUG=!SLUG:W=w!
set SLUG=!SLUG:X=x!
set SLUG=!SLUG:Y=y!
set SLUG=!SLUG:Z=z!

:: Convert consecutive spaces to single underscore
:clean_spaces
if "!SLUG!" neq "!SLUG:  =_!" (
    set SLUG=!SLUG:  =_!
    goto clean_spaces
)

:: Convert single spaces to underscores
set SLUG=!SLUG: =_!

:: Create folder path
set DIR=blog\%YEAR%\%MONTH%\%SLUG%
set PATH_MD=%DIR%\index.md
set FULL_PATH=content\%PATH_MD%

echo.
echo Creating %FULL_PATH%

:: Create directory
mkdir "%FULL_PATH%\.." 2>nul

:: Create file directly
echo --- > "%FULL_PATH%"
echo title: "%TITLE%" >> "%FULL_PATH%"
echo description: "" >> "%FULL_PATH%"
echo summary: "" >> "%FULL_PATH%"
echo date: %date%T%time%+09:00 >> "%FULL_PATH%"
echo lastmod: %date%T%time%+09:00 >> "%FULL_PATH%"
echo draft: true >> "%FULL_PATH%"
echo weight: 50 >> "%FULL_PATH%"
echo categories: [] >> "%FULL_PATH%"
echo tags: [] >> "%FULL_PATH%"
echo contributors: [] >> "%FULL_PATH%"
echo pinned: false >> "%FULL_PATH%"
echo homepage: false >> "%FULL_PATH%"
echo seo: >> "%FULL_PATH%"
echo   title: "" # custom title ^(optional^) >> "%FULL_PATH%"
echo   description: "" # custom description ^(recommended^) >> "%FULL_PATH%"
echo   canonical: "" # custom canonical URL ^(optional^) >> "%FULL_PATH%"
echo   robots: "" # custom robot tags ^(optional^) >> "%FULL_PATH%"
echo --- >> "%FULL_PATH%"
echo. >> "%FULL_PATH%"

echo.
echo Created: %FULL_PATH%
echo.
echo Please edit the file to add your content and update the front matter.
echo Note: Title in the file is set to: %TITLE%
