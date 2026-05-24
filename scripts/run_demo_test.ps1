$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$scriptDir = Join-Path $projectRoot "tools\studio_operator"
Set-Location $projectRoot

$venvPath = Join-Path $projectRoot ".venv_studio_operator"
$requirementsPath = Join-Path $scriptDir "requirements.txt"
$demoPath = Join-Path $scriptDir "demo_test_player.py"
$demoReportPath = Join-Path $projectRoot "logs\demo_test_report.md"
$recordingsPath = Join-Path $projectRoot "logs\recordings"

if (-not (Test-Path $venvPath)) {
	python -m venv $venvPath
}

$pythonExe = Join-Path $venvPath "Scripts\python.exe"

Write-Output ""
Write-Output "Demo test: 90 second recording"
Write-Output ""
Write-Output "Instructions:"
Write-Output "1. Close or restore old Roblox Studio windows if they are minimized."
Write-Output "2. The script will try to restore/maximize Studio."
Write-Output "3. When recording starts, click Studio and press Play/F5."
Write-Output ""

& $pythonExe -m pip install -r $requirementsPath -q
& $pythonExe $demoPath --mode manual-play-record --duration 90

Write-Output ""
Write-Output "Demo report: $demoReportPath"
Write-Output "Recordings: $recordingsPath"

