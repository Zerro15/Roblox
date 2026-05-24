#!/usr/bin/env powershell
# model_recommend.ps1 - Get model recommendation for a task

param(
    [Parameter(Mandatory=$true)]
    [string]$Task
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)

Write-Host "Analyzing task: $Task" -ForegroundColor Cyan

python "$ProjectRoot/tools/studio_operator/model_router.py" --task "$Task"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nTo start with Claude:" -ForegroundColor Yellow
    Write-Host "  claude --model [model]" -ForegroundColor Gray
    Write-Host "`nTo start with Codex:" -ForegroundColor Yellow
    Write-Host "  codex --profile [profile]" -ForegroundColor Gray
}
