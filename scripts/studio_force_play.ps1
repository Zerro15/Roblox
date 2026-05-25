$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$scriptDir = Join-Path $projectRoot "tools\studio_operator"
$venvPath = Join-Path $projectRoot ".venv_studio_operator"
$requirementsPath = Join-Path $scriptDir "requirements.txt"
$controllerPath = Join-Path $scriptDir "studio_play_controller.py"

Set-Location $projectRoot

if (-not (Test-Path $venvPath)) {
	python -m venv $venvPath
}

$pythonExe = Join-Path $venvPath "Scripts\python.exe"
& $pythonExe -m pip install -r $requirementsPath -q
& $pythonExe $controllerPath --mode force-play
