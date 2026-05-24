#!/usr/bin/env powershell
# prompt_show.ps1 - Show specific prompt content

param(
    [Parameter(Mandatory=$true)]
    [string]$Name
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$PromptsDir = "$ProjectRoot/prompts"

$promptFile = "$PromptsDir/$Name.md"

if (Test-Path $promptFile) {
    Write-Host "=== Prompt: $Name ===" -ForegroundColor Cyan
    Write-Host ""
    Get-Content $promptFile
    Write-Host ""
    Write-Host "=== End Prompt ===" -ForegroundColor Cyan
} else {
    Write-Host "Prompt not found: $Name" -ForegroundColor Red
    Write-Host "Available prompts:" -ForegroundColor Yellow
    & "$ScriptDir/prompt_list.ps1"
    exit 1
}
