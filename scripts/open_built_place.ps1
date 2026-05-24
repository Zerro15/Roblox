$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$placePath = Join-Path $projectRoot 'build\game.rbxlx'
if (-not (Test-Path $placePath)) {
	throw "Built place not found: $placePath"
}

$studioExe = Get-ChildItem "$env:LOCALAPPDATA\Roblox\Versions" -Filter 'RobloxStudioBeta.exe' -Recurse -ErrorAction SilentlyContinue |
	Sort-Object LastWriteTime -Descending |
	Select-Object -First 1

if (-not $studioExe) {
	throw "RobloxStudioBeta.exe not found in $env:LOCALAPPDATA\\Roblox\\Versions"
}

Start-Process -FilePath $studioExe.FullName -ArgumentList $placePath
Write-Output $studioExe.FullName
Write-Output $placePath
