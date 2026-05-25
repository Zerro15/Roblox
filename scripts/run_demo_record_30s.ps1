param(
	[switch]$AutoPlay,
	[switch]$Assisted
)

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

Write-Output ""
Write-Output "Quick demo test: 30 second recording"
Write-Output ""

if ($AutoPlay) {
	if ($Assisted) {
		Write-Output "Mode: Assisted auto-play"
		Write-Output "The runner will try to focus build\game.rbxlx Roblox Studio and press F5 after focus is confirmed."
	} else {
		Write-Output "Mode: Safe auto-play"
		Write-Output "The runner will focus Roblox Studio and press F5 only if Studio focus is confirmed."
	}
} else {
	Write-Output "Mode: Manual play"
	Write-Output "User must press Play/F5 manually when recording starts."
}

Write-Output ""
Write-Output "Instructions:"
Write-Output "1. Close or restore old Roblox Studio windows if they are minimized."
Write-Output "2. The script will try to restore/maximize Studio."
if ($AutoPlay -and $Assisted) {
	Write-Output "3. Do not touch mouse or keyboard during focus attempt."
	Write-Output "4. If auto focus fails, click Roblox Studio when prompted."
} elseif (-not $AutoPlay) {
	Write-Output "3. When recording starts, click Studio and press Play/F5."
}
Write-Output ""

& $pythonExe -m pip install -r $requirementsPath -q

if ($AutoPlay) {
	if ($Assisted) {
		& $pythonExe $demoPath --mode manual-play-record --duration 30 --auto-play --auto-play-mode assisted
	} else {
		& $pythonExe $demoPath --mode manual-play-record --duration 30 --auto-play --auto-play-mode safe
	}
} else {
	& $pythonExe $demoPath --mode manual-play-record --duration 30
}

Write-Output ""
Write-Output "Demo report: $demoReportPath"
Write-Output "Recordings: $recordingsPath"

