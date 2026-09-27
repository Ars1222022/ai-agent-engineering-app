$ErrorActionPreference = "Stop"

$WorkshopDir = $PSScriptRoot
$ProjectDir = Join-Path $WorkshopDir "lesson6-agent"
$Starter = Join-Path $ProjectDir "start-lesson6.ps1"

Write-Host "Lesson 6 project folder: $ProjectDir" -ForegroundColor Cyan

if (-not (Test-Path -LiteralPath $Starter)) {
    Write-Host "The lesson project is missing from this folder." -ForegroundColor Red
    Write-Host "Download or clone the complete workshop repository. This script will not create a second project elsewhere." -ForegroundColor Yellow
    exit 1
}

Set-Location $ProjectDir
& $Starter
