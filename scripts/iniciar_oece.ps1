param([int]$Puerto=8765)
$ErrorActionPreference='Stop'
$projectRootOECE=Split-Path -Parent $PSScriptRoot
$pythonOECE=Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $pythonOECE)) {
    Write-Host 'No se encontró Python del entorno. Revisa docs/USO_DIARIO.md para la instalación.'
    Read-Host 'Pulsa Entrar para cerrar'
    exit 1
}
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
