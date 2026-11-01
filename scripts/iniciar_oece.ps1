param([int]$Puerto=8765,[string]$Python='')
$ErrorActionPreference='Stop'
$projectRootOECE=Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot 'resolver_python.ps1')
$pythonOECE=Resolve-OECEPython -ExplicitPython $Python
$addressOECE="http://127.0.0.1:$Puerto"
$runningOECE=$false
try {
    $responseOECE=Invoke-WebRequest -UseBasicParsing -Uri "$addressOECE/api/casos" -TimeoutSec 2
    $runningOECE=($responseOECE.StatusCode -eq 200)
} catch {}
if (-not $runningOECE) {
    $logsOECE=Join-Path $projectRootOECE 'data\operacion\.oece'
    New-Item -ItemType Directory -Path $logsOECE -Force | Out-Null
    $processOECE=Start-Process -FilePath $pythonOECE -ArgumentList @('-m','oece','panel','--puerto',"$Puerto") -WorkingDirectory $projectRootOECE -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $logsOECE 'panel.log') -RedirectStandardError (Join-Path $logsOECE 'errores.log')
    $processOECE.Id | Set-Content -LiteralPath (Join-Path $logsOECE 'panel.pid')
    for ($attemptOECE=0; $attemptOECE -lt 20; $attemptOECE++) {
        Start-Sleep -Milliseconds 250
        try { if ((Invoke-WebRequest -UseBasicParsing -Uri "$addressOECE/api/casos" -TimeoutSec 1).StatusCode -eq 200) {$runningOECE=$true;break} } catch {}
    }
}
if (-not $runningOECE) { throw 'El panel no inició. Revisar data/operacion/.oece/errores.log' }
Start-Process $addressOECE
