#!/usr/bin/env powershell
# team_dry_run.ps1 - Build and test without opening Studio

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "=== Team Dry Run: Build Only ===" -ForegroundColor Cyan

# Build the game
Write-Host "`nBuilding game..." -ForegroundColor Yellow
& "$ProjectRoot/scripts/build_place.ps1"

# Check build result
$buildPath = "$ProjectRoot/build/game.rbxlx"
if (Test-Path $buildPath) {
    $buildSize = (Get-Item $buildPath).Length / 1MB
    Write-Host "`n✅ Build successful!" -ForegroundColor Green
    Write-Host "Build size: $([Math]::Round($buildSize, 2)) MB"
    Write-Host "Build path: $buildPath"
} else {
    Write-Host "`n❌ Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== End Dry Run ===" -ForegroundColor Cyan
Write-Host "`nBuild verified. Ready for demo test or merge." -ForegroundColor Gray
