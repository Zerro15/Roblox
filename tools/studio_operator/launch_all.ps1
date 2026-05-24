$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)
Set-Location $projectRoot

$venvPath = Join-Path $projectRoot '.venv_studio_operator'
$requirementsPath = Join-Path $scriptDir 'requirements.txt'
$operatorPath = Join-Path $scriptDir 'studio_operator.py'

if (-not (Test-Path $venvPath)) {
	python -m venv $venvPath
}

$pythonExe = Join-Path $venvPath 'Scripts\python.exe'

& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r $requirementsPath
& $pythonExe $operatorPath --click-mode off
