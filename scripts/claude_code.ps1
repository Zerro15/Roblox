#!/usr/bin/env powershell
# claude_code.ps1 - Start Claude with code (sonnet) model

Write-Host "Starting Claude with code model (sonnet)..." -ForegroundColor Cyan
Write-Host "Use this for: feature implementation, bug fixes, code review" -ForegroundColor Gray
Write-Host ""

claude --model sonnet
