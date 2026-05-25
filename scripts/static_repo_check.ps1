$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonScript = Join-Path $projectRoot "tools\studio_operator\static_repo_check.py"

Set-Location $projectRoot

python $pythonScript
