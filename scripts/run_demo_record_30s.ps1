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

Write-Output "Quick demo test: 30 second recording"
Write-Output "Recording will start first. Then click Roblox Studio and press Play/F5 manually."
& $pythonExe -m pip install -r $requirementsPath
& $pythonExe $demoPath --mode manual-play-record --duration 30
Write-Output ("Demo report: " + $demoReportPath)
Write-Output ("Recordings: " + $recordingsPath)
