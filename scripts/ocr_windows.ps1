param(
    [Parameter(Mandatory=$true)][string]$Root,
    [Parameter(Mandatory=$true)][string]$Job,
    [string]$Language = 'es-MX'
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.Streams.IRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.SoftwareBitmap,Windows.Graphics.Imaging,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrResult,Windows.Foundation,ContentType=WindowsRuntime] | Out-Null
[Windows.Globalization.Language,Windows.Globalization,ContentType=WindowsRuntime] | Out-Null

$basePath = (Resolve-Path -LiteralPath $Root).Path.TrimEnd('\') + '\'
function In-Root([string]$Path) {
    $absolute = [IO.Path]::GetFullPath($Path)
    if (-not $absolute.StartsWith($basePath, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Path outside task root'
    }
    return $absolute
}
function Hash-File([string]$Path) {
    $stream = [IO.File]::OpenRead($Path)
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($algorithm.ComputeHash($stream))).Replace('-', '').ToLowerInvariant()
    } finally {
        $algorithm.Dispose()
        $stream.Dispose()
    }
}
function Await-WinRT($Operation, [Type]$ResultType) {
    $method = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
        $_.Name -eq 'AsTask' -and $_.IsGenericMethodDefinition -and
        $_.GetParameters().Count -eq 1 -and
        $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
    } | Select-Object -First 1
    $task = $method.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.GetAwaiter().GetResult()
}

$jobPath = In-Root $Job
$request = [IO.File]::ReadAllText($jobPath, [Text.Encoding]::UTF8) | ConvertFrom-Json
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new($Language))
if ($null -eq $engine) { throw 'OCR language unavailable' }
$records = @()
foreach ($page in $request.pages) {
    $imagePath = In-Root $page.image_path
    $outputPath = In-Root $page.output_path
    $imageHash = Hash-File $imagePath
    if ($imageHash -ne $page.image_sha256) { throw 'Image hash mismatch before OCR' }
    $file = Await-WinRT ([Windows.Storage.StorageFile]::GetFileFromPathAsync($imagePath)) ([Windows.Storage.StorageFile])
    $stream = $null
    $bitmap = $null
    try {
        $stream = Await-WinRT ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
        $decoder = Await-WinRT ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bitmap = Await-WinRT ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        if ($bitmap.PixelWidth -gt [Windows.Media.Ocr.OcrEngine]::MaxImageDimension -or $bitmap.PixelHeight -gt [Windows.Media.Ocr.OcrEngine]::MaxImageDimension) {
            throw 'Image exceeds OCR dimensions'
        }
        $recognized = Await-WinRT ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
        $lines = @()
        foreach ($line in $recognized.Lines) {
            $words = @()
            foreach ($word in $line.Words) {
                $rect = $word.BoundingRect
                $words += [ordered]@{ text=$word.Text; x=$rect.X; y=$rect.Y; width=$rect.Width; height=$rect.Height }
            }
            $lines += [ordered]@{ text=$line.Text; words=$words }
        }
        if ((Hash-File $imagePath) -ne $imageHash) {
            throw 'Image changed during OCR'
        }
        $record = [ordered]@{
            schema_version='0.1'; source_sha256=$request.source_sha256; source_name=$request.source_name
            page_pdf=$page.page_pdf; image_sha256=$imageHash; image_path=$imagePath
            engine='Windows.Media.Ocr'; engine_version=$null; windows_build=[Environment]::OSVersion.Version.ToString()
            language=$engine.RecognizerLanguage.LanguageTag; width=$bitmap.PixelWidth; height=$bitmap.PixelHeight
            text=$recognized.Text; lines=$lines; confidence=$null; reviewed=$false; apta_para_evaluacion=$false
            warnings=@('OCR requires visual review; engine does not expose confidence score')
        }
        [IO.File]::WriteAllText($outputPath, ($record | ConvertTo-Json -Depth 12), [Text.UTF8Encoding]::new($false))
        $records += [ordered]@{page_pdf=$page.page_pdf; output=$outputPath; characters=$recognized.Text.Length}
    } finally {
        if ($null -ne $bitmap) { $bitmap.Dispose() }
        if ($null -ne $stream) { $stream.Dispose() }
    }
}
$records | ConvertTo-Json -Depth 4
