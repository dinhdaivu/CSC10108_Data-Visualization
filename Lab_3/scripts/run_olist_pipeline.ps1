$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$rawDir = Join-Path $projectRoot "data\raw"
$processedDir = Join-Path $projectRoot "data\processed"
$pythonExe = "C:\Users\Vu\AppData\Local\Python\bin\python.exe"
$kaggleExe = "C:\Users\Vu\AppData\Local\Python\pythoncore-3.14-64\Scripts\kaggle.exe"
$preprocessScript = Join-Path $projectRoot "scripts\preprocess_olist_for_powerbi.py"

New-Item -ItemType Directory -Force -Path $rawDir | Out-Null
New-Item -ItemType Directory -Force -Path $processedDir | Out-Null

& $kaggleExe datasets download -d olistbr/brazilian-ecommerce -p $rawDir --unzip
& $pythonExe $preprocessScript

Write-Host "Pipeline completed."
Write-Host "Raw data:" $rawDir
Write-Host "Processed data:" $processedDir
