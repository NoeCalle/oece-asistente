function Resolve-OECEPython {
    param([string]$ExplicitPython='')
    $projectRootOECE=Split-Path -Parent $PSScriptRoot
    $candidatesOECE=@()
    if ($ExplicitPython) {$candidatesOECE=@($ExplicitPython)}
    elseif ($env:OECE_PYTHON) {$candidatesOECE=@($env:OECE_PYTHON)}
    else {
        $candidatesOECE+=Join-Path $projectRootOECE '.venv\Scripts\python.exe'
        foreach ($nameOECE in @('python.exe','python3.exe','python','python3')) {
            $commandOECE=Get-Command $nameOECE -ErrorAction SilentlyContinue
            if ($commandOECE -and $commandOECE.Source -and $commandOECE.Source -notlike '*\WindowsApps\*') {$candidatesOECE+=$commandOECE.Source}
        }
        # Compatibilidad con la instalación anterior; no es requisito del motor.
        $candidatesOECE+=Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    }
    foreach ($candidateOECE in ($candidatesOECE | Select-Object -Unique)) {
        if (-not (Test-Path -LiteralPath $candidateOECE -PathType Leaf)) {continue}
        & $candidateOECE -c "import sys,pypdf,docx,PIL; sys.exit(0 if sys.version_info >= (3,12) else 1)" 2>$null
        if ($LASTEXITCODE -eq 0) {return (Resolve-Path -LiteralPath $candidateOECE).Path}
    }
    throw 'Se requiere Python 3.12 o posterior con las dependencias de requirements-indexacion.txt. Define OECE_PYTHON o usa -Python con la ruta del intérprete.'
}
