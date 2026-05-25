param(
	[int]$MaxAttempts = 3,
	[switch]$DiagnoseOnly
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$scriptDir = Join-Path $projectRoot "tools\studio_operator"
$venvPath = Join-Path $projectRoot ".venv_studio_operator"
$requirementsPath = Join-Path $scriptDir "requirements.txt"
$pythonScript = Join-Path $scriptDir "demo_autofix_loop.py"

Set-Location $projectRoot

Write-Output ""
Write-Output "Demo autofix loop"
Write-Output "Close extra Roblox Studio windows if possible."
Write-Output "Keep only build\game.rbxlx - Roblox Studio if manual intervention is needed."
Write-Output "The loop will not merge PR, force push, delete files, or commit generated artifacts."
Write-Output ""

if (-not (Test-Path $venvPath)) {
	python -m venv $venvPath
}

$pythonExe = Join-Path $venvPath "Scripts\python.exe"
& $pythonExe -m pip install -r $requirementsPath -q

if ($DiagnoseOnly) {
	& $pythonExe $pythonScript --mode diagnose
} else {
	& $pythonExe $pythonScript --mode loop --max-attempts $MaxAttempts
}

Write-Output ""
Write-Output "Autofix report: $(Join-Path $projectRoot 'logs\demo_autofix_report.md')"
