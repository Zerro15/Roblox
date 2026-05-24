$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$buildDir = Join-Path $projectRoot 'build'
New-Item -ItemType Directory -Force -Path $buildDir | Out-Null

$rojo = Get-Command rojo -ErrorAction SilentlyContinue
if (-not $rojo) {
	$localRojoPath = Join-Path $env:LOCALAPPDATA 'Programs\Rojo\rojo.exe'
	if (Test-Path $localRojoPath) {
		$rojo = Get-Item $localRojoPath
	}
}

if (-not $rojo) {
	throw "Rojo executable not found."
}

$outputPath = Join-Path $buildDir 'game.rbxlx'
if ($rojo -is [System.Management.Automation.CommandInfo]) {
	& $rojo.Source build .\default.project.json -o $outputPath
} else {
	& $rojo.FullName build .\default.project.json -o $outputPath
}

if (-not (Test-Path $outputPath)) {
	throw "Build output not found: $outputPath"
}

Write-Output $outputPath
