# ============================================================
# Lektion 6 — Verifieringsscript
# Anvander projektets venv-Python for att undvika fel Python.
# ============================================================

$ProjectDir = $PSScriptRoot
$venvPython = Join-Path $ProjectDir "venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "[ERROR] venv saknas. Kor setup-lesson6.ps1 forst." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== LESSON 6 ENVIRONMENT CHECK ===" -ForegroundColor Cyan
Write-Host ""

Push-Location $ProjectDir
try {

$allOk = $true

function Test-Import {
    param([string]$Label, [string]$Module)
    & $venvPython -c "import $Module" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] $Label" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] $Label" -ForegroundColor Red
        $script:allOk = $false
    }
}

Test-Import "Agents SDK" "agents"
Test-Import "openai" "openai"
Test-Import "requests" "requests"
Test-Import "tools.course_tools" "tools.course_tools"
Test-Import "mcp_server.server" "mcp_server.server"

Write-Host ""
Write-Host "Kor pytest..." -ForegroundColor Yellow
& $venvPython -m pytest tests/ -q

if ($LASTEXITCODE -ne 0) {
    $allOk = $false
}

Write-Host ""
if ($env:OPENAI_API_KEY) {
    Write-Host "[OK] OPENAI_API_KEY ar satt" -ForegroundColor Green
} else {
    Write-Host "[INFO] OPENAI_API_KEY saknas - Block 5-9 kraver nyckel" -ForegroundColor Yellow
}

Write-Host ""
if ($allOk) {
    Write-Host "=== CHECK KLAR ===" -ForegroundColor Green
    exit 0
} else {
    Write-Host "=== CHECK MISSLYCKADES ===" -ForegroundColor Red
    Write-Host "Stoppa och kontakta lararen." -ForegroundColor Yellow
    Write-Host "Kor INTE setup-lesson6.ps1 igen efter att du borjat andra projektfiler." -ForegroundColor Yellow
    exit 1
}
}
finally {
    Pop-Location
}
