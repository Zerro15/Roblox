#!/usr/bin/env powershell
# prompt_list.ps1 - List available prompts

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$PromptsDir = "$ProjectRoot/prompts"

Write-Host "=== Available Prompts ===" -ForegroundColor Cyan

if (Test-Path $PromptsDir) {
    $prompts = Get-ChildItem $PromptsDir -Filter "*.md" | Sort-Object Name

    Write-Host "`nPrompt Library:" -ForegroundColor Yellow
    foreach ($prompt in $prompts) {
        $name = $prompt.BaseName
        $size = $prompt.Length
        Write-Host "  • $name ($size bytes)"
    }

    Write-Host "`nUsage:" -ForegroundColor Yellow
    Write-Host "  .\prompt_show.ps1 -Name <prompt_name>" -ForegroundColor Gray
    Write-Host "  Example: .\prompt_show.ps1 -Name design_feature" -ForegroundColor Gray
} else {
    Write-Host "Prompts directory not found: $PromptsDir" -ForegroundColor Red
}

Write-Host "`n=== End List ===" -ForegroundColor Cyan
