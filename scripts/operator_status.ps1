$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$scriptDir = Join-Path $projectRoot 'tools\studio_operator'
Set-Location $projectRoot

$venvPath = Join-Path $projectRoot '.venv_studio_operator'
if (-not (Test-Path $venvPath)) {
	python -m venv $venvPath
}

$pythonExe = Join-Path $venvPath 'Scripts\python.exe'
$requirementsPath = Join-Path $scriptDir 'requirements.txt'
$flowPath = Join-Path $scriptDir 'studio_flow.py'

Write-Output "=== bridge/rojo/studio status ==="
& $pythonExe -m pip install -r $requirementsPath
& $pythonExe $flowPath --flow status --click-mode off
Write-Output "=== git status ==="
if (Test-Path .\.git) {
	git status --short
} else {
	Write-Output "No local .git repo in project root yet."
}
Write-Output "=== gh auth status ==="
gh auth status 2>$null
Write-Output "=== last screenshots ==="
Get-ChildItem .\logs\screenshots -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 5 Name,LastWriteTime
Write-Output "=== last reports ==="
Get-ChildItem .\logs\*.md -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 5 Name,LastWriteTime
