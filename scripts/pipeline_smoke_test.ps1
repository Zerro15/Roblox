$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Output ""
Write-Output "Pipeline smoke test: validates build, files, logs, reports, recordings"
Write-Output "Does NOT launch Roblox Studio. Does NOT fake results."
Write-Output ""

$pythonScript = Join-Path $projectRoot "tools\studio_operator\pipeline_smoke_test.py"

$venvPython = Join-Path $projectRoot ".venv_studio_operator\Scripts\python.exe"
if (Test-Path $venvPython) {
    & $venvPython $pythonScript
} else {
    python $pythonScript
}

Write-Output ""
Write-Output "Report: $(Join-Path $projectRoot 'logs\pipeline_smoke_report.md')"
