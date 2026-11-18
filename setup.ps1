function Invoke-HypocriticalSaintSetup {
    param(
        [string]$InstallDir = "",
        [switch]$NoLaunch = $false,
        [switch]$Force = $false
    )

    $ErrorActionPreference = "Stop"

    function Write-Banner {
        Write-Host ""
        Write-Host "==============================================================================" -ForegroundColor DarkRed
        Write-Host "                           HYPOCRITICAL SAINT" -ForegroundColor Yellow
        Write-Host "                   Digital Image Steganography Studio" -ForegroundColor White
        Write-Host "             'Innocent on the Outside. Secret on the Inside.'" -ForegroundColor Gray
        Write-Host "==============================================================================" -ForegroundColor DarkRed
        Write-Host "  Author:     Um Al-Baneen Awwad" -ForegroundColor DarkGray
        Write-Host "  Course:     Digital Image Processing (4th Year Computer Engineering)" -ForegroundColor DarkGray
        Write-Host "  University: University of Basrah" -ForegroundColor DarkGray
        Write-Host "==============================================================================" -ForegroundColor DarkRed
        Write-Host ""
    }

    function Show-Troubleshooting([string]$ErrorMessage) {
        Write-Host ""
        Write-Host "------------------------------------------------------------------------------" -ForegroundColor Red
        Write-Host " [!] SETUP ENCOUNTERED AN ISSUE:" -ForegroundColor Red
        Write-Host "     $ErrorMessage" -ForegroundColor Yellow
        Write-Host "------------------------------------------------------------------------------" -ForegroundColor Red
        Write-Host " Troubleshooting Steps:" -ForegroundColor White
        Write-Host " 1. Make sure Python 3.10, 3.11, or 3.12 is installed:" -ForegroundColor Gray
        Write-Host "    Download from: https://www.python.org/downloads/" -ForegroundColor Gray
        Write-Host "    Or install via Windows Terminal: winget install Python.Python.3.11" -ForegroundColor Cyan
        Write-Host "    (Be sure to check 'Add Python to PATH' during installation)" -ForegroundColor Yellow
        Write-Host " 2. Ensure Git is installed or network connection is active:" -ForegroundColor Gray
        Write-Host "    https://git-scm.com/download/win" -ForegroundColor Gray
        Write-Host " 3. You can retry setup anytime by executing:" -ForegroundColor Gray
        Write-Host "    irm https://raw.githubusercontent.com/xdc7-css/Hypocritical-Saint/main/setup.ps1 | iex" -ForegroundColor Cyan
        Write-Host "------------------------------------------------------------------------------" -ForegroundColor Red
        Write-Host ""
    }

    try {
        Write-Banner

        # 1. Environment & OS Verification
        Write-Host "[1/7] Inspecting Windows Environment..." -ForegroundColor Cyan
        if (-not $IsWindows -and -not $env:OS -like "*Windows*") {
            throw "HYPOCRITICAL SAINT installer is designed for Windows 10 and Windows 11."
        }
        Write-Host "      [OK] Windows OS verified ($([Environment]::OSVersion.VersionString))." -ForegroundColor Green

        # 2. Python Detection (Search for Python 3.10 - 3.12)
        Write-Host "[2/7] Detecting Compatible Python Engine..." -ForegroundColor Cyan
        $PythonExe = ""
        $PythonExtraArg = ""
        $PythonVersionStr = ""

        function Test-Py([string]$Cmd, [string]$ExtraArg) {
            try {
                if ($Cmd -like "*\*" -and -not (Test-Path $Cmd)) { return $null }
                $output = if ($ExtraArg) {
                    & $Cmd $ExtraArg -c "import sys; print(sys.version.split()[0])" 2>$null
                } else {
                    & $Cmd -c "import sys; print(sys.version.split()[0])" 2>$null
                }
                if ($LASTEXITCODE -eq 0 -and $output) {
                    $v = $output.Trim().Split(".")
                    if ([int]$v[0] -eq 3 -and [int]$v[1] -ge 10) {
                        return $output.Trim()
                    }
                }
            } catch {}
            return $null
        }

        $Candidates = @(
            @{ Exe = "py"; Arg = "-3.12" },
            @{ Exe = "py"; Arg = "-3.11" },
            @{ Exe = "py"; Arg = "-3.10" },
            @{ Exe = "py"; Arg = "-3" },
            @{ Exe = "python"; Arg = "" },
            @{ Exe = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"; Arg = "" },
            @{ Exe = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"; Arg = "" },
            @{ Exe = "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe"; Arg = "" },
            @{ Exe = "C:\Python312\python.exe"; Arg = "" },
            @{ Exe = "C:\Python311\python.exe"; Arg = "" },
            @{ Exe = "C:\Python310\python.exe"; Arg = "" }
        )

        foreach ($c in $Candidates) {
            $ver = Test-Py $c.Exe $c.Arg
            if ($ver) {
                $PythonExe = $c.Exe
                $PythonExtraArg = $c.Arg
                $PythonVersionStr = $ver
                break
            }
        }

        if (-not $PythonExe) {
            throw "No compatible Python installation found. Python 3.10, 3.11, or 3.12 is required."
        }
        $DisplayCmd = if ($PythonExtraArg) { "$PythonExe $PythonExtraArg" } else { $PythonExe }
        Write-Host "      [OK] Python $PythonVersionStr found ($DisplayCmd)." -ForegroundColor Green

        # 3. Target Installation Directory Determination
        Write-Host "[3/7] Determining Installation Directory..." -ForegroundColor Cyan
        $RepoUrl = "https://github.com/xdc7-css/Hypocritical-Saint.git"
        $ZipUrl  = "https://github.com/xdc7-css/Hypocritical-Saint/archive/refs/heads/main.zip"

        $IsLocalSource = $false
        if ([string]::IsNullOrWhiteSpace($InstallDir)) {
            if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "app.py"))) {
                $InstallDir = $PSScriptRoot
                $IsLocalSource = $true
                Write-Host "      [*] Detected existing local project source at: $InstallDir" -ForegroundColor Yellow
            } else {
                # Check for Drive D:
                $HasDriveD = $false
                try {
                    if (Test-Path "D:\") {
                        $HasDriveD = $true
                    }
                } catch {
                    $HasDriveD = $false
                }

                if ($HasDriveD) {
                    $InstallDir = "D:\Hypocritical-Saint"
                    Write-Host "      [*] Default drive D: detected. Installing to: $InstallDir" -ForegroundColor Green
                } else {
                    $InstallDir = "C:\Hypocritical-Saint"
                    Write-Host "      [!] Drive D: not found on this system. Falling back to: $InstallDir" -ForegroundColor Yellow
                }
            }
        } else {
            Write-Host "      [*] Using custom installation path: $InstallDir" -ForegroundColor Green
        }

        # 4. Clone or Extract Source Files
        Write-Host "[4/7] Preparing Project Files..." -ForegroundColor Cyan
        if ($IsLocalSource) {
            Write-Host "      [OK] Using local project files in $InstallDir." -ForegroundColor Green
        } elseif (Test-Path (Join-Path $InstallDir "app.py")) {
            Write-Host "      [OK] Project files already exist at $InstallDir." -ForegroundColor Green
            if (Test-Path (Join-Path $InstallDir ".git")) {
                try {
                    Write-Host "      [*] Checking for latest updates via Git..." -ForegroundColor DarkGray
                    git -C $InstallDir pull --quiet 2>$null
                } catch {}
            }
        } else {
            if (-not (Test-Path $InstallDir)) {
                New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
            }

            $HasGit = $false
            try {
                $gitVer = git --version 2>$null
                if ($LASTEXITCODE -eq 0 -and $gitVer) {
                    $HasGit = $true
                }
            } catch {
                $HasGit = $false
            }

            if ($HasGit) {
                Write-Host "      [*] Cloning project from GitHub ($RepoUrl)..." -ForegroundColor Cyan
                git clone --depth 1 $RepoUrl $InstallDir
                if ($LASTEXITCODE -ne 0) {
                    throw "Failed to clone repository from $RepoUrl."
                }
            } else {
                Write-Host "      [*] Git not detected. Downloading source package from GitHub..." -ForegroundColor Cyan
                $TempZip = Join-Path $env:TEMP "hypocritical_saint_source.zip"
                $TempExtract = Join-Path $env:TEMP "hypocritical_saint_extract"

                if (Test-Path $TempExtract) { Remove-Item -Recurse -Force $TempExtract }
                
                [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13
                Invoke-WebRequest -Uri $ZipUrl -OutFile $TempZip -UseBasicParsing
                
                Expand-Archive -Path $TempZip -DestinationPath $TempExtract -Force
                $UnzippedRoot = Join-Path $TempExtract "Hypocritical-Saint-main"
                if (Test-Path $UnzippedRoot) {
                    Copy-Item -Path "$UnzippedRoot\*" -Destination $InstallDir -Recurse -Force
                } else {
                    $SubFolder = (Get-ChildItem $TempExtract | Where-Object { $_.PSIsContainer } | Select-Object -First 1).FullName
                    Copy-Item -Path "$SubFolder\*" -Destination $InstallDir -Recurse -Force
                }
                Remove-Item -Force $TempZip -ErrorAction SilentlyContinue
                Remove-Item -Recurse -Force $TempExtract -ErrorAction SilentlyContinue
            }
            Write-Host "      [OK] Project files successfully placed in $InstallDir." -ForegroundColor Green
        }

        # 5. Virtual Environment & Dependencies Setup
        Write-Host "[5/7] Configuring Dedicated Virtual Environment (.venv)..." -ForegroundColor Cyan
        $VenvPath = Join-Path $InstallDir ".venv"
        $VenvPython = Join-Path $VenvPath "Scripts\python.exe"

        if (-not (Test-Path $VenvPython)) {
            Write-Host "      [*] Creating virtual environment in $VenvPath..." -ForegroundColor Cyan
            if ($PythonExtraArg) {
                & $PythonExe $PythonExtraArg -m venv $VenvPath
            } else {
                & $PythonExe -m venv $VenvPath
            }
            if (-not (Test-Path $VenvPython)) {
                throw "Failed to create virtual environment at $VenvPath."
            }
            Write-Host "      [OK] Virtual environment created successfully." -ForegroundColor Green
        } else {
            Write-Host "      [OK] Existing virtual environment detected." -ForegroundColor Green
        }

        Write-Host "[*] Upgrading pip inside virtual environment..." -ForegroundColor DarkGray
        & $VenvPython -m pip install --upgrade pip --quiet

        Write-Host "[*] Installing HYPOCRITICAL SAINT package and dependencies..." -ForegroundColor Cyan
        & $VenvPython -m pip install -e $InstallDir --quiet
        & $VenvPython -m pip install gradio --quiet

        # 6. Automated Functional Verification
        Write-Host "[6/7] Running Verification and Diagnostic Checks..." -ForegroundColor Cyan
        $VerifyOutput = & $VenvPython -c "import sys, stegano, gradio, PIL, cv2, numpy; print('ALL_MODULES_OK')" 2>&1
        if ($VerifyOutput -notmatch "ALL_MODULES_OK") {
            throw "Module verification failed: $VerifyOutput"
        }
        Write-Host "      [OK] Core Steganography algorithms, Gradio UI, and image processing modules verified." -ForegroundColor Green

        # 7. Global CLI Command Configuration (PROJECT RUN)
        Write-Host "[7/7] Registering Global 'PROJECT RUN' Command..." -ForegroundColor Cyan
        
        try {
            Set-ItemProperty -Path "HKCU:\Environment" -Name "HYPOCRITICAL_SAINT_HOME" -Value $InstallDir -Force
        } catch {}
        $env:HYPOCRITICAL_SAINT_HOME = $InstallDir

        $UserPath = (Get-ItemProperty -Path "HKCU:\Environment" -Name "Path" -ErrorAction SilentlyContinue).Path
        $PathEntries = if ($UserPath) { $UserPath -split ";" } else { @() }
        if ($PathEntries -notcontains $InstallDir) {
            $NewUserPath = if ([string]::IsNullOrWhiteSpace($UserPath)) { $InstallDir } else { "$UserPath;$InstallDir" }
            try {
                Set-ItemProperty -Path "HKCU:\Environment" -Name "Path" -Value $NewUserPath -Force
            } catch {}
            $env:Path = "$env:Path;$InstallDir"
            Write-Host "      [OK] Added '$InstallDir' to persistent User PATH." -ForegroundColor Green
        }

        $WindowsAppsDir = Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps"
        if (Test-Path $WindowsAppsDir) {
            $SourceCmd = Join-Path $InstallDir "PROJECT.cmd"
            if (Test-Path $SourceCmd) {
                Copy-Item -Path $SourceCmd -Destination (Join-Path $WindowsAppsDir "PROJECT.cmd") -Force -ErrorAction SilentlyContinue
                Write-Host "      [OK] Registered 'PROJECT.cmd' for instant global execution." -ForegroundColor Green
            }
        }

        # Summary Display
        Write-Host ""
        Write-Host "==============================================================================" -ForegroundColor Green
        Write-Host "               HYPOCRITICAL SAINT INSTALLED SUCCESSFULLY!                     " -ForegroundColor Green
        Write-Host "==============================================================================" -ForegroundColor Green
        Write-Host "  Installation Path : $InstallDir" -ForegroundColor White
        Write-Host "  Web Interface     : http://127.0.0.1:7860" -ForegroundColor Cyan
        Write-Host "  Global Command    : PROJECT RUN" -ForegroundColor Yellow
        Write-Host "------------------------------------------------------------------------------" -ForegroundColor DarkGray
        Write-Host "  You can launch the studio at any time from ANY command prompt or PowerShell:" -ForegroundColor White
        Write-Host "    > PROJECT RUN" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  Additional Commands:" -ForegroundColor White
        Write-Host "    > PROJECT STATUS    (Check if local studio server is running)" -ForegroundColor Gray
        Write-Host "    > PROJECT HELP      (Display usage and options)" -ForegroundColor Gray
        Write-Host "==============================================================================" -ForegroundColor Green
        Write-Host ""

        if (-not $NoLaunch) {
            $IsPortRunning = $false
            try {
                $conn = Get-NetTCPConnection -LocalPort 7860 -State Listen -ErrorAction SilentlyContinue
                if ($conn) { $IsPortRunning = $true }
            } catch {
                $IsPortRunning = $false
            }

            if ($IsPortRunning) {
                Write-Host "[*] HYPOCRITICAL SAINT is already running at http://127.0.0.1:7860" -ForegroundColor Green
                Write-Host "[*] Opening browser..." -ForegroundColor Cyan
                Start-Process "http://127.0.0.1:7860"
            } else {
                Write-Host "[*] Launching HYPOCRITICAL SAINT server..." -ForegroundColor Green
                Write-Host "[*] Opening web browser at http://127.0.0.1:7860 ..." -ForegroundColor Cyan
                
                Start-Process -FilePath $VenvPython -ArgumentList "app.py" -WorkingDirectory $InstallDir -WindowStyle Minimized
                Start-Sleep -Seconds 2
                Start-Process "http://127.0.0.1:7860"
            }
        }

    } catch {
        Show-Troubleshooting $_.Exception.Message
        exit 1
    }
}

Invoke-HypocriticalSaintSetup @args
