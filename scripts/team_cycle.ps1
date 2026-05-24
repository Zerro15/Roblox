#!/usr/bin/env powershell
# team_cycle.ps1 - Full development cycle

param(
    [switch]$SkipDemo = $false
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "=== Team Cycle: Full Development Workflow ===" -ForegroundColor Cyan

# Step 1: Status
Write-Host "`n[Step 1/4] Checking team status..." -ForegroundColor Yellow
& "$ProjectRoot/scripts/team_status.ps1"

# Step 2: Plan
Write-Host "`n[Step 2/4] Planning next tasks..." -ForegroundColor Yellow
& "$ProjectRoot/scripts/team_plan_next.ps1"

# Step 3: Dry Run
Write-Host "`n[Step 3/4] Running dry build..." -ForegroundColor Yellow
& "$ProjectRoot/scripts/team_dry_run.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Build failed. Cycle stopped." -ForegroundColor Red
    exit 1
}

# Step 4: Demo (optional)
if (-not $SkipDemo) {
    Write-Host "`n[Step 4/4] Running demo test..." -ForegroundColor Yellow
    & "$ProjectRoot/scripts/team_review_demo.ps1"
} else {
    Write-Host "`n[Step 4/4] Skipping demo test (--SkipDemo flag)" -ForegroundColor Yellow
}

Write-Host "`n=== Cycle Complete ===" -ForegroundColor Cyan
Write-Host "`nNext steps:" -ForegroundColor Gray
Write-Host "  1. Review test results"
Write-Host "  2. If approved: Run pr_safe_merge.ps1"
Write-Host "  3. If issues: Fix and re-run cycle"
