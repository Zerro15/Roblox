#!/usr/bin/env powershell
# team_status.ps1 - Check team status

param(
    [switch]$Verbose = $false
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "=== Team Status ===" -ForegroundColor Cyan

# Git status
Write-Host "`n[Git Status]" -ForegroundColor Yellow
$branch = git branch --show-current
$status = git status --short
$commits = git log --oneline -3

Write-Host "Branch: $branch"
if ($status) {
    Write-Host "Uncommitted changes: $(($status | Measure-Object).Count) files"
} else {
    Write-Host "Working tree: Clean"
}
Write-Host "Recent commits:"
$commits | ForEach-Object { Write-Host "  $_" }

# PR status
Write-Host "`n[Pull Requests]" -ForegroundColor Yellow
$prs = gh pr list --state open --json number,title,state
if ($prs) {
    $prCount = ($prs | ConvertFrom-Json | Measure-Object).Count
    Write-Host "Open PRs: $prCount"
    $prs | ConvertFrom-Json | ForEach-Object {
        Write-Host "  #$($_.number) - $($_.title)"
    }
} else {
    Write-Host "Open PRs: 0"
}

# Game state
Write-Host "`n[Game State]" -ForegroundColor Yellow
$stateFile = "$ProjectRoot/docs/team/CURRENT_STATE.md"
if (Test-Path $stateFile) {
    Write-Host "Current state documented in: docs/team/CURRENT_STATE.md"
    Write-Host "Features implemented:"
    Select-String "✅" $stateFile | Select-Object -First 5 | ForEach-Object {
        Write-Host "  $($_.Line.Trim())"
    }
} else {
    Write-Host "State file not found"
}

# Build status
Write-Host "`n[Build Status]" -ForegroundColor Yellow
$buildPath = "$ProjectRoot/build/game.rbxlx"
if (Test-Path $buildPath) {
    $buildDate = (Get-Item $buildPath).LastWriteTime
    $buildSize = (Get-Item $buildPath).Length / 1MB
    Write-Host "Build exists: Yes"
    Write-Host "Build date: $buildDate"
    Write-Host "Build size: $([Math]::Round($buildSize, 2)) MB"
} else {
    Write-Host "Build exists: No"
}

# Test status
Write-Host "`n[Test Status]" -ForegroundColor Yellow
$reportPath = "$ProjectRoot/logs/demo_test_report.md"
if (Test-Path $reportPath) {
    $reportDate = (Get-Item $reportPath).LastWriteTime
    Write-Host "Last test: $reportDate"
    $status = Select-String "Status:" $reportPath | Select-Object -First 1
    if ($status) {
        Write-Host "Last status: $($status.Line.Trim())"
    }
} else {
    Write-Host "No test report found"
}

Write-Host "`n=== End Status ===" -ForegroundColor Cyan
