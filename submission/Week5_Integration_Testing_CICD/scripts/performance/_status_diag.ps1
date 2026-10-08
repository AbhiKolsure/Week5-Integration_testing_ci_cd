$ErrorActionPreference = 'SilentlyContinue'
$root = 'c:\Performance Testing\week4_performance_load_testing'
$outDir = Join-Path -Path $root -ChildPath 'artifacts\performance\after'
Write-Output ('outDir exists: ' + (Test-Path -LiteralPath $outDir))

$one = Get-ChildItem -LiteralPath $outDir -Directory | Where-Object { $_.Name -eq 'baseline-1000-u50-get-tasks-stats-r2' } | Select-Object -First 1
if (-not $one) {
    Write-Output 'TARGET RUN DIR NOT FOUND'
    exit
}

Write-Output ('type: ' + $one.GetType().FullName)
Write-Output ('ToString: [' + $one.ToString() + ']')
Write-Output ('FullName: [' + $one.FullName + ']')
Write-Output ('Name: [' + $one.Name + ']')

$countViaObject = @(Get-ChildItem -LiteralPath $one -Recurse -File -Force).Count
Write-Output ('count via object : ' + $countViaObject)
$countViaFullName = @(Get-ChildItem -LiteralPath $one.FullName -Recurse -File -Force).Count
Write-Output ('count via FullName: ' + $countViaFullName)

$joinViaObject = Join-Path -Path $one -ChildPath 'summary.json'
Write-Output ('joinpath via object  : [' + $joinViaObject + '] exists=' + (Test-Path -LiteralPath $joinViaObject))
$joinViaFullName = Join-Path -Path $one.FullName -ChildPath 'summary.json'
Write-Output ('joinpath via FullName: [' + $joinViaFullName + '] exists=' + (Test-Path -LiteralPath $joinViaFullName))
