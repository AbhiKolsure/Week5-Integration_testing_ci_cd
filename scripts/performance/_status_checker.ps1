# _status_checker.ps1
# Explicit, prompt-free status checker for performance run directories.
#
# Fixes applied:
#   1) Always use $dirInfo.FullName (a string) for path operations. In this
#      environment DirectoryInfo.ToString() returns ONLY the leaf name, which made
#      Get-ChildItem / Join-Path resolve relative to the current directory and
#      silently report 0 files / all-MISSING for every run.
#   2) Never call Write-Output without an explicit argument. A bare "Write-Output;"
#      makes PowerShell prompt for the mandatory InputObject[0] parameter, which
#      blocks non-interactive status checks ("Supply values for ... InputObject[0]").
#   3) No $_ inside nested expressions; explicit variables + Join-Path / -LiteralPath.
#   4) Missing directories are reported explicitly via Test-Path guards (no prompts,
#      no terminating errors).

$ErrorActionPreference = 'SilentlyContinue'

$projectRoot = (Resolve-Path -LiteralPath (Join-Path -Path $PSScriptRoot -ChildPath '..\..')).Path
$perfRoot = Join-Path -Path $projectRoot -ChildPath 'artifacts\performance'
$afterRoot = Join-Path -Path $perfRoot -ChildPath 'after'
$coreArtifacts = @('summary.json', 'locust_report.html', 'locust_stdout.txt', 'locust_stats.csv')

function Show-RunStatus {
    param(
        [string]$RunPath,
        [string]$RunName
    )

    if (-not (Test-Path -LiteralPath $RunPath)) {
        Write-Output ('Run: ' + $RunName)
        Write-Output '  Directory: MISSING'
        Write-Output '  Status: INCOMPLETE (directory not found)'
        Write-Output ''
        return
    }

    $fileList = @(Get-ChildItem -LiteralPath $RunPath -Recurse -File -Force)
    $subDirList = @(Get-ChildItem -LiteralPath $RunPath -Directory -Force)

    $presentList = @()
    $missingList = @()
    foreach ($artifactName in $coreArtifacts) {
        $artifactPath = Join-Path -Path $RunPath -ChildPath $artifactName
        if (Test-Path -LiteralPath $artifactPath) {
            $presentList += $artifactName
        } else {
            $missingList += $artifactName
        }
    }

    $presentText = $presentList -join ', '
    if ($presentText -eq '') { $presentText = '(none)' }
    $missingText = $missingList -join ', '
    if ($missingText -eq '') { $missingText = '(none)' }
    if ($missingList.Count -eq 0) {
        $statusText = 'COMPLETE'
    } else {
        $statusText = 'INCOMPLETE'
    }

    Write-Output ('Run: ' + $RunName)
    Write-Output ('  Total files: ' + $fileList.Count + ' | Subdirs: ' + $subDirList.Count)
    Write-Output ('  Required artifacts present: ' + $presentText)
    Write-Output ('  Required artifacts missing: ' + $missingText)
    Write-Output ('  Status: ' + $statusText)
    Write-Output ''
}

Write-Output '=== PERFORMANCE RUN STATUS CHECKER (FIXED) ==='
Write-Output ('Project root: ' + $projectRoot)
Write-Output ''
Write-Output '###### ORIGINAL BASELINE DIRECTORIES ######'

$perfRootExists = Test-Path -LiteralPath $perfRoot
if (-not $perfRootExists) {
    Write-Output ('MISSING: ' + $perfRoot)
}
if ($perfRootExists) {
    $baselineDirs = @()
    $topLevelDirs = @(Get-ChildItem -LiteralPath $perfRoot -Directory -Force)
    foreach ($dirInfo in $topLevelDirs) {
        if ($dirInfo.Name -like '*baseline*') {
            $baselineDirs += $dirInfo
        }
    }
    $sortedBaselineDirs = @($baselineDirs | Sort-Object -Property Name)
    foreach ($dirInfo in $sortedBaselineDirs) {
        Show-RunStatus -RunPath $dirInfo.FullName -RunName $dirInfo.Name
    }

    Write-Output '###### BASELINE AGGREGATE FILES ######'
    foreach ($fileName in @('baseline_summary.json', 'baseline_1000_tasks.txt', 'baseline_10000_tasks.txt')) {
        $filePath = Join-Path -Path $perfRoot -ChildPath $fileName
        if (Test-Path -LiteralPath $filePath) {
            Write-Output ('  ' + $fileName + ': PRESENT')
        } else {
            Write-Output ('  ' + $fileName + ': MISSING')
        }
    }
    Write-Output ''
}

Write-Output '###### POST-OPTIMIZATION RUN DIRECTORIES (after) ######'
$afterRootExists = Test-Path -LiteralPath $afterRoot
if (-not $afterRootExists) {
    Write-Output ('MISSING: ' + $afterRoot)
}
if ($afterRootExists) {
    $afterDirs = @(Get-ChildItem -LiteralPath $afterRoot -Directory -Force | Sort-Object -Property Name)
    foreach ($dirInfo in $afterDirs) {
        Show-RunStatus -RunPath $dirInfo.FullName -RunName $dirInfo.Name
    }
}
Write-Output ''
Write-Output '=== END OF STATUS CHECK ==='

