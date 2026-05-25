$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Output ""
Write-Output "Quick demo test with assisted auto-play: 30 second recording"
Write-Output ""

& powershell -ExecutionPolicy Bypass -File .\scripts\run_demo_record_30s.ps1 -AutoPlay -Assisted
