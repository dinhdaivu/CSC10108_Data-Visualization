$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$rawDir = Join-Path $projectRoot "football\raw"
$processedDir = Join-Path $projectRoot "football\processed"
$pythonExe = "C:\Users\Vu\AppData\Local\Python\bin\python.exe"
$kaggleExe = "C:\Users\Vu\AppData\Local\Python\pythoncore-3.14-64\Scripts\kaggle.exe"
$preprocessScript = Join-Path $projectRoot "scripts\preprocess_football_for_powerbi.py"

New-Item -ItemType Directory -Force -Path $rawDir | Out-Null
New-Item -ItemType Directory -Force -Path $processedDir | Out-Null

& $kaggleExe datasets download -d hugomathien/soccer -p $rawDir --unzip
& $pythonExe $preprocessScript

Write-Host "Football pipeline completed."
Write-Host "Raw data:" $rawDir
Write-Host "Processed data:" $processedDir
