# Cursor Studio - core logic (no UI). Dot-sourced by CursorStudio.ps1 and by the self-test.
# Works in Windows PowerShell 5.1 (built into Windows 11). No admin rights needed: everything is per-user (HKCU).

Set-StrictMode -Version 2.0

$script:RegKey      = 'HKCU:\Control Panel\Cursors'
$script:SchemesKey  = 'HKCU:\Control Panel\Cursors\Schemes'
# Registry value order Windows uses inside a scheme string (17 roles, Windows 10/11).
$script:RoleOrder   = 'Arrow','Help','AppStarting','Wait','Crosshair','IBeam','NWPen','No','SizeNS','SizeWE','SizeNWSE','SizeNESW','SizeAll','UpArrow','Hand','Pin','Person'

$script:WindowsDefault = [ordered]@{
    Arrow       = '%SystemRoot%\cursors\aero_arrow.cur'
    Help        = '%SystemRoot%\cursors\aero_helpsel.cur'
    AppStarting = '%SystemRoot%\cursors\aero_working.ani'
    Wait        = '%SystemRoot%\cursors\aero_busy.ani'
    Crosshair   = ''
    IBeam       = ''
    NWPen       = '%SystemRoot%\cursors\aero_pen.cur'
    No          = '%SystemRoot%\cursors\aero_unavail.cur'
    SizeNS      = '%SystemRoot%\cursors\aero_ns.cur'
    SizeWE      = '%SystemRoot%\cursors\aero_ew.cur'
    SizeNWSE    = '%SystemRoot%\cursors\aero_nwse.cur'
    SizeNESW    = '%SystemRoot%\cursors\aero_nesw.cur'
    SizeAll     = '%SystemRoot%\cursors\aero_move.cur'
    UpArrow     = '%SystemRoot%\cursors\aero_up.cur'
    Hand        = '%SystemRoot%\cursors\aero_link.cur'
    Pin         = '%SystemRoot%\cursors\aero_pin.cur'
    Person      = '%SystemRoot%\cursors\aero_person.cur'
}

function Get-StudioHome {
    $base = $env:LOCALAPPDATA
    if (-not $base) { $base = [IO.Path]::GetTempPath() }
    Join-Path $base 'CursorStudio'
}

function Get-CursorCatalog {
    param([Parameter(Mandatory)][string]$Root)   # folder that contains catalog.json
    $file = Join-Path $Root 'catalog.json'
    if (-not (Test-Path -LiteralPath $file)) { throw "catalog.json not found in '$Root'." }
    Get-Content -LiteralPath $file -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Get-CursorStyle {
    param([Parameter(Mandatory)]$Catalog, [Parameter(Mandatory)][string]$Set, [string]$Style = 'A')
    $item = $Catalog.sets | Where-Object { $_.slug -eq $Set -or [string]$_.num -eq $Set -or $_.name -eq $Set } | Select-Object -First 1
    if (-not $item) { throw "Unknown set '$Set'. Run with -List to see the names." }
    $st = $item.styles | Where-Object { $_.key -eq $Style } | Select-Object -First 1
    if (-not $st) { throw "Set '$($item.name)' has no style '$Style' (use A, B, C, C2, GA, GB or GC)." }
    [pscustomobject]@{ Set = $item; Style = $st }
}

# --- thin registry wrappers (tests replace these) -----------------------------------------
function Write-CursorValue([string]$Name, [string]$Value) {
    if ($Name -eq '') { $Name = '(default)' }
    if (-not (Test-Path -LiteralPath $script:RegKey)) { New-Item -Path $script:RegKey -Force | Out-Null }
    Set-ItemProperty -LiteralPath $script:RegKey -Name $Name -Value $Value -Type String
}
function Write-CursorDword([string]$Name, [int]$Value) {
    Set-ItemProperty -LiteralPath $script:RegKey -Name $Name -Value $Value -Type DWord
}
function Read-CursorValue([string]$Name) {
    if ($Name -eq '') { $Name = '(default)' }
    try { (Get-ItemProperty -LiteralPath $script:RegKey -Name $Name -ErrorAction Stop).$Name } catch { $null }
}
function Write-SchemeValue([string]$Name, [string]$Value) {
    if (-not (Test-Path -LiteralPath $script:SchemesKey)) { New-Item -Path $script:SchemesKey -Force | Out-Null }
    Set-ItemProperty -LiteralPath $script:SchemesKey -Name $Name -Value $Value -Type ExpandString
}
function Send-CursorRefresh {
    if (-not ('CursorStudio.Native' -as [type])) {
        Add-Type -Namespace CursorStudio -Name Native -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("user32.dll", SetLastError = true)]
public static extern bool SystemParametersInfo(uint uiAction, uint uiParam, System.IntPtr pvParam, uint fWinIni);
'@
    }
    # SPI_SETCURSORS = 0x57, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE = 0x03
    [void][CursorStudio.Native]::SystemParametersInfo(0x57, 0, [IntPtr]::Zero, 0x03)
}

function Backup-CurrentCursors {
    $home_ = Get-StudioHome
    $file  = Join-Path $home_ 'backup.json'
    if (Test-Path -LiteralPath $file) { return }          # keep the very first (original) backup
    New-Item -ItemType Directory -Force -Path $home_ | Out-Null
    $snap = [ordered]@{ Scheme = (Read-CursorValue ''); }
    foreach ($r in $script:RoleOrder) { $snap[$r] = Read-CursorValue $r }
    $snap | ConvertTo-Json | Set-Content -LiteralPath $file -Encoding UTF8
}

function Install-CursorSet {
    <#
      Copies one style variant into %LOCALAPPDATA%\CursorStudio\Installed, registers it in
      Mouse Properties > Pointers > Scheme, and (with -Apply) makes it the active scheme right now.
    #>
    param(
        [Parameter(Mandatory)][string]$Root, [Parameter(Mandatory)]$Catalog, [Parameter(Mandatory)]$Set, [Parameter(Mandatory)]$Style,
        [Parameter(Mandatory)][ValidateSet('Animated','Static')][string]$Mode,
        [switch]$Apply
    )
    $src = Join-Path (Join-Path $Root $Style.path) $Mode
    if (-not (Test-Path -LiteralPath $src)) { throw "Cursor folder not found: $src" }
    $ext   = if ($Mode -eq 'Animated') { '.ani' } else { '.cur' }
    $label = "$($Style.scheme) ($Mode)"
    $dest  = Join-Path (Join-Path (Get-StudioHome) 'Installed') ("$($Set.slug)-$($Style.key)-$Mode")
    New-Item -ItemType Directory -Force -Path $dest | Out-Null

    $paths = [ordered]@{}
    foreach ($role in $Catalog.roles) {
        $f = Join-Path $src ($role.file + $ext)
        if (-not (Test-Path -LiteralPath $f)) { throw "Missing cursor file: $f" }
        Copy-Item -LiteralPath $f -Destination $dest -Force
        $paths[$role.registry] = Join-Path $dest ($role.file + $ext)
    }
    foreach ($r in $script:RoleOrder) { if (-not $paths.Contains($r)) { throw "Style '$label' has no '$r' cursor." } }

    Backup-CurrentCursors
    Write-SchemeValue $label (($script:RoleOrder | ForEach-Object { $paths[$_] }) -join ',')
    if ($Apply) {
        foreach ($r in $script:RoleOrder) { Write-CursorValue $r $paths[$r] }
        Write-CursorValue '' $label
        Write-CursorDword 'Scheme Source' 1
        Send-CursorRefresh
    }
    [pscustomobject]@{ Label = $label; Folder = $dest; Applied = [bool]$Apply }
}

function Restore-WindowsCursors {
    foreach ($r in $script:RoleOrder) { Write-CursorValue $r $script:WindowsDefault[$r] }
    Write-CursorValue '' 'Windows Default'
    Write-CursorDword 'Scheme Source' 2
    Send-CursorRefresh
}

function Restore-OriginalCursors {
    $file = Join-Path (Get-StudioHome) 'backup.json'
    if (-not (Test-Path -LiteralPath $file)) { Restore-WindowsCursors; return 'Windows Default' }
    $b = Get-Content -LiteralPath $file -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($r in $script:RoleOrder) {
        $prop = $b.PSObject.Properties[$r]
        $v = if ($prop) { $prop.Value } else { '' }
        if ($null -eq $v) { $v = '' }
        Write-CursorValue $r ([string]$v)
    }
    $name = [string]$b.Scheme
    Write-CursorValue '' $name
    Send-CursorRefresh
    if ($name) { $name } else { 'previous cursors' }
}
