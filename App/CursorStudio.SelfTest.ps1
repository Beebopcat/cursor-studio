# Self-test for the Cursor Studio core logic. Uses an in-memory registry stub and a temp profile folder,
# so it is safe to run anywhere (it never touches the real registry): pwsh App/CursorStudio.SelfTest.ps1
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'CursorStudio.Core.ps1')
$root = Split-Path -Parent $PSScriptRoot
$env:LOCALAPPDATA = Join-Path ([IO.Path]::GetTempPath()) ('cs-selftest-' + [guid]::NewGuid().ToString('N'))

$script:reg = @{}; $script:schemes = @{}; $script:refresh = 0
function Write-CursorValue([string]$Name, [string]$Value) { $script:reg[$Name] = $Value }
function Write-CursorDword([string]$Name, [int]$Value) { $script:reg[$Name] = $Value }
function Read-CursorValue([string]$Name) { $script:reg[$Name] }
function Write-SchemeValue([string]$Name, [string]$Value) { $script:schemes[$Name] = $Value }
function Send-CursorRefresh { $script:refresh++ }

$fail = 0; $n = 0
function Check($ok, $msg) { if (-not $ok) { "  FAIL $msg"; $script:fail++ } }

$cat = Get-CursorCatalog -Root $root
Check ($cat.sets.Count -eq 24) "catalog lists 24 sets ($($cat.sets.Count))"
foreach ($item in $cat.sets) {
    Check ($item.styles.Count -eq 7) "$($item.slug) has 7 styles"
    Check ((($item.styles | ForEach-Object { $_.key }) -join ',') -eq 'A,B,C,C2,GA,GB,GC') "$($item.slug) style keys are A,B,C,C2,GA,GB,GC"
    foreach ($st in $item.styles) {
        foreach ($mode in 'Animated', 'Static') {
            $ext = if ($mode -eq 'Animated') { '.ani' } else { '.cur' }
            $res = Install-CursorSet -Root $root -Catalog $cat -Set $item -Style $st -Mode $mode -Apply
            $bad = @($script:RoleOrder | Where-Object { -not ($script:reg[$_] -like "*$ext") -or -not (Test-Path -LiteralPath $script:reg[$_]) })
            Check ($bad.Count -eq 0) "$($item.slug) $($st.key) [$mode] applied all 17 files"
            Check ($script:schemes[$res.Label].Split(',').Count -eq 17) "$($item.slug) $($st.key) [$mode] scheme has 17 paths"
            $n++
        }
    }
}
$pick = Get-CursorStyle -Catalog $cat -Set '24' -Style 'C2'
Check ($pick.Style.key -eq 'C2' -and $pick.Set.num -eq 24) 'Get-CursorStyle resolves by number'
$pick = Get-CursorStyle -Catalog $cat -Set '7' -Style 'GB'
Check ($pick.Style.key -eq 'GB' -and $pick.Set.num -eq 7 -and $pick.Style.source -eq 'gemini') 'Get-CursorStyle resolves a Gemini style (GB)'
$threw = $false; try { Get-CursorStyle -Catalog $cat -Set '7' -Style 'GZ' | Out-Null } catch { $threw = $true }
Check $threw 'Get-CursorStyle rejects an unknown style key'
Check ($script:refresh -eq $n) "SPI refresh sent for each apply ($script:refresh of $n)"
Restore-WindowsCursors
Check ($script:reg['Arrow'] -like '*aero_arrow.cur' -and $script:reg[''] -eq 'Windows Default') 'Restore-WindowsCursors resets the scheme'
Remove-Item -Recurse -Force $env:LOCALAPPDATA
if ($fail) { "$fail check(s) failed"; exit 1 } else { "ALL CHECKS PASSED ($n installs)" }
