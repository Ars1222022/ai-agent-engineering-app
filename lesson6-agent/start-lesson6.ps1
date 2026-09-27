$ErrorActionPreference = "Stop"

$PhysicalProjectDir = $PSScriptRoot
$ProjectDir = $PhysicalProjectDir
$VenvDir = Join-Path $ProjectDir "venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$Requirements = Join-Path $ProjectDir "requirements.txt"

function Use-ShortProjectPath {
    if ($PhysicalProjectDir.Length -le 120) {
        return $true
    }

    $driveMarker = Join-Path $PhysicalProjectDir ".lesson6-drive"
    if (Test-Path -LiteralPath $driveMarker) {
        $markerValue = (Get-Content -LiteralPath $driveMarker -Raw).Trim()
        $markerParts = $markerValue -split '\|', 2
        $preferredDrive = $markerParts[0]
        $markerToken = if ($markerParts.Count -eq 2) { $markerParts[1] } else { [guid]::NewGuid().ToString("N") }
    } else {
        $markerToken = [guid]::NewGuid().ToString("N")
        $markerValue = "|$markerToken"
        Set-Content -LiteralPath $driveMarker -Value $markerValue -Encoding ASCII
        $preferredDrive = $null
    }

    if ($preferredDrive -match '^[D-Z]$') {
        $driveIsMapped = [bool](Get-PSDrive -Name $preferredDrive -ErrorAction SilentlyContinue)
        if (-not $driveIsMapped) {
            & subst.exe "$preferredDrive`:" $PhysicalProjectDir | Out-Null
            $driveIsMapped = ($LASTEXITCODE -eq 0)
        }
        if ($driveIsMapped) {
            $aliasRoot = $preferredDrive + ":\"
            $aliasMarker = Join-Path $aliasRoot ".lesson6-drive"
            if ((Test-Path -LiteralPath $aliasMarker) -and ((Get-Content -LiteralPath $aliasMarker -Raw).Trim() -eq $markerValue)) {
                $script:ProjectDir = $aliasRoot
            }
        }
    }

    if ($script:ProjectDir -eq $PhysicalProjectDir) {
        $candidates = [char[]]([int][char]'Z'..[int][char]'D') | ForEach-Object { [string]$_ }
        foreach ($letter in $candidates) {
            if (Get-PSDrive -Name $letter -ErrorAction SilentlyContinue) { continue }
            & subst.exe "$letter`:" $PhysicalProjectDir | Out-Null
            if ($LASTEXITCODE -ne 0) { continue }

            $aliasRoot = $letter + ":\"
            $aliasMarker = Join-Path $aliasRoot ".lesson6-drive"
            if ((Test-Path -LiteralPath $aliasMarker) -and ((Get-Content -LiteralPath $aliasMarker -Raw).Trim() -eq $markerValue)) {
                $script:ProjectDir = $aliasRoot
                Set-Content -LiteralPath $driveMarker -Value "$letter|$markerToken" -Encoding ASCII
                break
            }

            & subst.exe "$letter`:" /d | Out-Null
        }
    }

    if ($script:ProjectDir -eq $PhysicalProjectDir) {
        Write-Host "Could not create a short Windows path alias for this project." -ForegroundColor Red
        Write-Host "No project files were moved. Free a drive letter or use Docker." -ForegroundColor Yellow
        return $false
    }

    $script:VenvDir = Join-Path $script:ProjectDir "venv"
    $script:VenvPython = Join-Path $script:VenvDir "Scripts\python.exe"
    $script:Requirements = Join-Path $script:ProjectDir "requirements.txt"
    Write-Host "Using a temporary drive alias for this same project folder: $script:ProjectDir" -ForegroundColor Cyan
    Write-Host "All project files and packages will remain in: $PhysicalProjectDir" -ForegroundColor Cyan
    return $true
}

function New-LocalEnvironment {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "Python was not found. Install Python 3.11 or newer, then run this script again." -ForegroundColor Red
        return $false
    }
    python -c "import sys; raise SystemExit(sys.version_info < (3, 11))" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python 3.11 or newer is required for local mode. Install it, then run this script again." -ForegroundColor Red
        return $false
    }

    $temporaryDir = Join-Path $ProjectDir ".tmp-install"
    New-Item -ItemType Directory -Path $temporaryDir -Force | Out-Null
    $previousTemp = $env:TEMP
    $previousTmp = $env:TMP
    try {
        $env:TEMP = $temporaryDir
        $env:TMP = $temporaryDir

        Write-Host "Creating the project's virtual environment inside the project folder..." -ForegroundColor Cyan
        & (Get-Command python).Source -m venv $VenvDir | Out-Host
        if ($LASTEXITCODE -ne 0) { return $false }

        Write-Host "Installing packages into the project venv (no global install or pip cache)..." -ForegroundColor Cyan
        & $VenvPython -m pip install --no-cache-dir -r $Requirements 2>&1 | Tee-Object -Variable pipOutput | Out-Host
        if ($LASTEXITCODE -ne 0) {
            if (($pipOutput | Out-String) -match "WinError 206|filename or extension is too long") {
                Write-Host "Windows still reported a path-length error. The project remains in its folder; try Docker." -ForegroundColor Red
            } else {
                Write-Host "Package installation failed. Check the error above and your internet connection." -ForegroundColor Red
            }
            return $false
        }
        return $true
    }
    finally {
        $env:TEMP = $previousTemp
        $env:TMP = $previousTmp
        if (Test-Path $temporaryDir) {
            Remove-Item -LiteralPath $temporaryDir -Recurse -Force
        }
    }
}

function Test-DockerAvailable {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Host "Docker was not found. Install Docker Desktop and start it, then try again." -ForegroundColor Red
        return $false
    }

    docker compose version | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker Compose is unavailable. Update or start Docker Desktop." -ForegroundColor Red
        return $false
    }
    return $true
}

function Initialize-LocalEnvironment {
    if (-not (Use-ShortProjectPath)) { return $false }

    $pywin32Pth = Join-Path $VenvDir "Lib\site-packages\pywin32.pth"
    $pywin32Bootstrap = Join-Path $VenvDir "Lib\site-packages\pywin32_bootstrap.py"
    if ((Test-Path $pywin32Pth) -and -not (Test-Path $pywin32Bootstrap)) {
        Write-Host "The local venv has an incomplete pywin32 install (pywin32.pth references a missing module)." -ForegroundColor Red
        $answer = Read-Host "Preserve it as a backup and create a clean venv? [y/N]"
        if ($answer -notin @("y", "Y")) {
            Write-Host "Local setup was not changed. Choose Docker from this menu to avoid the broken venv." -ForegroundColor Yellow
            return $false
        }

        $backupName = "venv-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Rename-Item -LiteralPath $VenvDir -NewName $backupName
        Write-Host "Preserved the previous environment as $backupName." -ForegroundColor Yellow
        if (-not (New-LocalEnvironment)) { return $false }
    }
    elseif (-not (Test-Path $VenvPython)) {
        if (-not (New-LocalEnvironment)) { return $false }
    }

    & $VenvPython -c "import sys; raise SystemExit(sys.version_info < (3, 11))" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "The existing venv uses an unsupported Python version. Preserve or recreate it, then retry." -ForegroundColor Red
        return $false
    }

    $checkOutput = & $VenvPython -c "import agents, openai, fastmcp, pytest, dotenv, requests" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing project packages. This can take a few minutes on first run..." -ForegroundColor Cyan
        $temporaryDir = Join-Path $ProjectDir ".tmp-install"
        New-Item -ItemType Directory -Path $temporaryDir -Force | Out-Null
        $previousTemp = $env:TEMP
        $previousTmp = $env:TMP
        try {
            $env:TEMP = $temporaryDir
            $env:TMP = $temporaryDir
            & $VenvPython -m pip install --no-cache-dir -r $Requirements 2>&1 | Tee-Object -Variable pipOutput | Out-Host
            $installExitCode = $LASTEXITCODE
        }
        finally {
            $env:TEMP = $previousTemp
            $env:TMP = $previousTmp
            if (Test-Path $temporaryDir) {
                Remove-Item -LiteralPath $temporaryDir -Recurse -Force
            }
        }
        if ($installExitCode -ne 0) {
            if (($pipOutput | Out-String) -match "WinError 206|filename or extension is too long") {
                Write-Host "Windows still reported a path-length error. The project remains in its folder; try Docker." -ForegroundColor Red
            } else {
                Write-Host "Package installation failed. Check the error above, your internet connection, and try again." -ForegroundColor Red
            }
            return $false
        }
        $checkOutput = & $VenvPython -c "import agents, openai, fastmcp, pytest, dotenv, requests" 2>&1
    }

    if (($LASTEXITCODE -ne 0) -or (($checkOutput | Out-String) -match "Error processing line.*pywin32\.pth")) {
        Write-Host ($checkOutput | Out-String) -ForegroundColor Red
        Write-Host "Python reports a broken package startup hook. Use Docker from the main menu, or ask the instructor to repair the local Python environment." -ForegroundColor Red
        return $false
    }
    return $true
}

Set-Location $ProjectDir

while ($true) {
    Write-Host ""
    Write-Host "=== Lesson 6: AI Agent Engineering ===" -ForegroundColor Cyan
    Write-Host "1) Start the local lesson menu (checks and demos)"
    Write-Host "2) Run automated tests"
    Write-Host "3) Build the Docker image"
    Write-Host "4) Start the lesson menu in Docker"
    Write-Host "0) Exit"
    $choice = Read-Host "Choose an option"

    switch ($choice) {
        "1" {
            if (Initialize-LocalEnvironment) {
                Push-Location $ProjectDir
                try { & $VenvPython (Join-Path $ProjectDir "lab_launcher.py") }
                finally { Pop-Location }
            }
        }
        "2" {
            if (Initialize-LocalEnvironment) {
                Push-Location $ProjectDir
                try { & $VenvPython -m pytest -q }
                finally { Pop-Location }
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "Some tests failed; read the test output above." -ForegroundColor Red
                }
            }
        }
        "3" {
            if (Test-DockerAvailable) {
                Set-Location $PhysicalProjectDir
                docker compose build lesson6
            }
        }
        "4" {
            if (Test-DockerAvailable) {
                Set-Location $PhysicalProjectDir
                docker compose run --build --rm lesson6
            }
        }
        "0" { return }
        default { Write-Host "Choose 0, 1, 2, 3, or 4." -ForegroundColor Yellow }
    }
}