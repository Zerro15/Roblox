#!/usr/bin/env powershell
# team_plan_next.ps1 - Plan next tasks

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "=== Team Plan: Next Tasks ===" -ForegroundColor Cyan

$nextActionsFile = "$ProjectRoot/docs/team/NEXT_ACTIONS.md"
if (Test-Path $nextActionsFile) {
    Write-Host "`nNext 5 Tasks (from NEXT_ACTIONS.md):" -ForegroundColor Yellow

    # Extract task names and priorities
    $content = Get-Content $nextActionsFile -Raw
    $tasks = $content -split "### Task \d+:" | Select-Object -Skip 1

    $taskNum = 1
    foreach ($task in $tasks | Select-Object -First 5) {
        $lines = $task -split "`n"
        $title = $lines[0].Trim()
        $priority = $lines[1] -match "Priority.*" ? $matches[0] : "Unknown"
        $effort = $lines[2] -match "Effort.*" ? $matches[0] : "Unknown"

        Write-Host "`n[$taskNum] $title" -ForegroundColor Green
        Write-Host "  $priority"
        Write-Host "  $effort"
        $taskNum++
    }
} else {
    Write-Host "NEXT_ACTIONS.md not found" -ForegroundColor Red
}

Write-Host "`n=== End Plan ===" -ForegroundColor Cyan
Write-Host "`nFor detailed planning, see: docs/team/NEXT_ACTIONS.md" -ForegroundColor Gray
