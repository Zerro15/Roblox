#!/usr/bin/env powershell
# claude_deep.ps1 - Start Claude with deep (opus/opusplan) model

Write-Host "Starting Claude with deep model (opusplan)..." -ForegroundColor Cyan
Write-Host "Use this for: architecture, security, complex debugging, risky operations" -ForegroundColor Gray
Write-Host ""

# Try opusplan first, fall back to opus if not available
$model = "opusplan"
Write-Host "Attempting to use $model..." -ForegroundColor Yellow

try {
    claude --model $model
} catch {
    Write-Host "opusplan not available, trying opus..." -ForegroundColor Yellow
    claude --model opus
}
