$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$rojo = Get-Command rojo -ErrorAction SilentlyContinue
if (-not $rojo) {
	$localRojoPath = Join-Path $env:LOCALAPPDATA 'Programs\Rojo\rojo.exe'
	if (Test-Path $localRojoPath) {
		$rojo = Get-Item $localRojoPath
	}
}

if (-not $rojo) {
	Write-Host "Rojo is not installed or not available in PATH or the local Rojo folder."
	Write-Host "Install options:"
	Write-Host "  aftman add rojo-rbx/rojo"
	Write-Host "  cargo install rojo"
	Write-Host "  https://github.com/rojo-rbx/rojo/releases"
	exit 1
}

if ($rojo -is [System.Management.Automation.CommandInfo]) {
	& $rojo.Source serve .\default.project.json
} else {
	& $rojo.FullName serve .\default.project.json
}
