# ============================================================
# Lektion 6 — LM Studio testscript
# ============================================================

Write-Host ""
Write-Host "=== LM STUDIO TEST ===" -ForegroundColor Cyan
Write-Host ""

function Test-LMStudioModels {
    try {
        $response = Invoke-RestMethod `
            -Uri "http://localhost:1234/v1/models" `
            -Method Get `
            -TimeoutSec 5

        if ($response.data.Count -gt 0) {
            $model = $response.data[0].id
            Write-Host "[OK] Model found: $model" -ForegroundColor Green
            return $model
        }
    }
    catch {}

    Write-Host "[ERROR] LM Studio not reachable or no models" -ForegroundColor Red
    Write-Host "[INFO] Starta LM Studio -> Developer -> Start Server" -ForegroundColor Yellow
    return $null
}

function Test-LMStudioInference {
    param([string]$Model)

    $body = @{
        model = $Model
        messages = @(
            @{ role = "user"; content = "Say OK" }
        )
        max_tokens = 10
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod `
            -Uri "http://localhost:1234/v1/chat/completions" `
            -Method Post `
            -Body $body `
            -ContentType "application/json" `
            -TimeoutSec 30

        Write-Host "[OK] LM Studio inference: $($response.choices[0].message.content)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "[ERROR] LM Studio inference failed" -ForegroundColor Red
        return $false
    }
}

$model = Test-LMStudioModels
if ($model) {
    Test-LMStudioInference -Model $model
}

Write-Host ""
Write-Host "=== TEST KLAR ===" -ForegroundColor Cyan
