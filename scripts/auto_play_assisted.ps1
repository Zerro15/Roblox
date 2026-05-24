$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$scriptDir = Join-Path $projectRoot 'tools\studio_operator'
Set-Location $projectRoot

$venvPath = Join-Path $projectRoot '.venv_studio_operator'
$requirementsPath = Join-Path $scriptDir 'requirements.txt'
$flowPath = Join-Path $scriptDir 'studio_flow.py'

if (-not (Test-Path $venvPath)) {
	python -m venv $venvPath
}

$pythonExe = Join-Path $venvPath 'Scripts\python.exe'

Write-Output "Click Roblox Studio when prompted. Operator will only press F5 if Studio focus is confirmed."
& $pythonExe -m pip install -r $requirementsPath
& $pythonExe $flowPath --flow build-open-play --click-mode cautious --focus-mode assisted
