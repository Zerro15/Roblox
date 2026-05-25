$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Output ""
Write-Output "Quick demo test with assisted auto-play: 30 second recording"
Write-Output ""
Write-Output "The runner will try to focus the correct build\game.rbxlx Roblox Studio window automatically."
Write-Output "Do not touch mouse or keyboard during focus attempt."
Write-Output "If auto focus fails, click Roblox Studio when prompted."
Write-Output ""

& powershell -ExecutionPolicy Bypass -File .\scripts\run_demo_record_30s.ps1 -AutoPlay -Assisted
