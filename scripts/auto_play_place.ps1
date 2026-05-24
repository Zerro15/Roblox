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

Write-Output "Operator will only press F5 if Roblox Studio focus is confirmed."
& $pythonExe -m pip install -r $requirementsPath
& $pythonExe $flowPath --flow full-safe --click-mode cautious
