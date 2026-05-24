#!/usr/bin/env powershell
# team_review_demo.ps1 - Run demo test and review

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "=== Team Review: Demo Test ===" -ForegroundColor Cyan

# Run the demo test
Write-Host "`nRunning demo test..." -ForegroundColor Yellow
& "$ProjectRoot/scripts/run_demo_test.ps1"

# Check results
Write-Host "`nDemo test complete. Checking results..." -ForegroundColor Yellow

$reportPath = "$ProjectRoot/logs/demo_test_report.md"
if (Test-Path $reportPath) {
    Write-Host "`nTest Report:" -ForegroundColor Green
    Get-Content $reportPath | Select-Object -First 20
    Write-Host "`n... (see full report in logs/demo_test_report.md)" -ForegroundColor Gray
} else {
    Write-Host "Test report not found" -ForegroundColor Red
}

# Check for videos
$recordingsDir = "$ProjectRoot/logs/recordings"
if (Test-Path $recordingsDir) {
    $videos = Get-ChildItem $recordingsDir -Filter "*.mp4" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($videos) {
        Write-Host "`nLatest recording: $($videos.Name)" -ForegroundColor Green
    }
}

Write-Host "`n=== End Review ===" -ForegroundColor Cyan
