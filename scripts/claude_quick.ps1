#!/usr/bin/env powershell
# claude_quick.ps1 - Start Claude with quick (haiku) model

Write-Host "Starting Claude with quick model (haiku)..." -ForegroundColor Cyan
Write-Host "Use this for: docs, status, simple scripts, summarization" -ForegroundColor Gray
Write-Host ""

claude --model haiku
