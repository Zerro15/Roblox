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
$operatorPath = Join-Path $scriptDir 'studio_operator.py'

& $pythonExe -m pip install -r $requirementsPath
& $pythonExe $operatorPath --action git-pr --click-mode off
