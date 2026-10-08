# _status_summary.ps1
# Compact one-line-per-run display of the same status logic as _status_checker.ps1.
# Uses $dirInfo.FullName (never object ToString()) and never calls bare Write-Output.

$ErrorActionPreference = 'SilentlyContinue'

$projectRoot = (Resolve-Path -LiteralPath (Join-Path -Path $PSScriptRoot -ChildPath '..\..')).Path
$perfRoot = Join-Path -Path $projectRoot -ChildPath 'artifacts\performance'
$afterRoot = Join-Path -Path $perfRoot -ChildPath 'after'
$coreArtifacts = @('summary.json', 'locust_report.html', 'locust_stdout.txt', 'locust_stats.csv')

function Get-RunLine {
    param(
        [string]$RunPath,
        [string]$RunName
    )

    if (-not (Test-Path -LiteralPath $RunPath)) {
        Write-Output ($RunName + ' | files=n/a | dir=MISSING | status=INCOMPLETE')
        return
    }

    $fileCount = @(Get-ChildItem -LiteralPath $RunPath -Recurse -File -Force).Count
    $subDirCount = @(Get-ChildItem -LiteralPath $RunPath -Directory -Force).Count

    $missingList = @()
    foreach ($artifactName in $coreArtifacts) {
        $artifactPath = Join-Path -Path $RunPath -ChildPath $artifactName
        if (-not (Test-Path -LiteralPath $artifactPath)) {
            $missingList += $artifactName
        }
    }

    if ($missingList.Count -eq 0) {
        $missingText = 'none'
        $statusText = 'COMPLETE'
    } else {
        $missingText = $missingList -join '+'
        $statusText = 'INCOMPLETE'
    }

    Write-Output ($RunName + ' | files=' + $fileCount + ' | subdirs=' + $subDirCount + ' | missing=' + $missingText + ' | status=' + $statusText)
}

Write-Output '=== COMPACT RUN STATUS SUMMARY ==='
Write-Output ''
Write-Output '--- ORIGINAL BASELINE DIRECTORIES (artifacts/performance/*baseline*) ---'

$baselineDirs = @()
$topLevelDirs = @(Get-ChildItem -LiteralPath $perfRoot -Directory -Force)
foreach ($dirInfo in $topLevelDirs) {
    if ($dirInfo.Name -like '*baseline*') {
        $baselineDirs += $dirInfo
    }
}
$sortedBaselineDirs = @($baselineDirs | Sort-Object -Property Name)
foreach ($dirInfo in $sortedBaselineDirs) {
    Get-RunLine -RunPath $dirInfo.FullName -RunName $dirInfo.Name
}
Write-Output ('baseline dir count: ' + $sortedBaselineDirs.Count)

Write-Output ''
Write-Output '--- BASELINE AGGREGATE FILES ---'
foreach ($fileName in @('baseline_summary.json', 'baseline_1000_tasks.txt', 'baseline_10000_tasks.txt')) {
    $filePath = Join-Path -Path $perfRoot -ChildPath $fileName
    if (Test-Path -LiteralPath $filePath) {
        Write-Output ($fileName + ': PRESENT')
    } else {
        Write-Output ($fileName + ': MISSING')
    }
}

Write-Output ''
Write-Output '--- POST-OPTIMIZATION RUN DIRECTORIES (artifacts/performance/after/*) ---'
$afterDirs = @(Get-ChildItem -LiteralPath $afterRoot -Directory -Force | Sort-Object -Property Name)
foreach ($dirInfo in $afterDirs) {
    Get-RunLine -RunPath $dirInfo.FullName -RunName $dirInfo.Name
}
Write-Output ('after dir count: ' + $afterDirs.Count)

Write-Output ''
Write-Output '=== END ==='
