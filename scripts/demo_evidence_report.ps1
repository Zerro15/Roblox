$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonScript = Join-Path $projectRoot "tools\studio_operator\demo_evidence_report.py"
$venvPython = Join-Path $projectRoot ".venv_studio_operator\Scripts\python.exe"

Set-Location $projectRoot

Write-Output ""
Write-Output "Demo evidence report"
Write-Output "Reads existing pipeline/demo reports and writes a clean reviewer summary."
Write-Output "Does NOT launch Roblox Studio. Does NOT copy videos or generated artifacts."
Write-Output ""

if (Test-Path $venvPython) {
    & $venvPython $pythonScript
} else {
    python $pythonScript
}

Write-Output ""
Write-Output "Evidence report: $(Join-Path $projectRoot 'logs\demo_evidence_report.md')"
