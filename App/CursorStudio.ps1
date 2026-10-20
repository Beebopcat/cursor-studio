<#
  Cursor Studio - dark-mode cursor installer for Windows 11 (24 sets x 4 styles, animated or static).
  Double-click Launch-CursorStudio.bat (or run this file with PowerShell).

  Headless usage (no window):
    .\CursorStudio.ps1 -List
    .\CursorStudio.ps1 -Set 01-Crystal-Dawn -Style A -Mode Animated -Apply
    .\CursorStudio.ps1 -Set 24 -Style C2 -Mode Static -InstallOnly
    .\CursorStudio.ps1 -Restore
#>
[CmdletBinding()]
param(
    [string]$Set,
    [ValidateSet('A','B','C','C2')][string]$Style = 'A',
    [ValidateSet('Animated','Static')][string]$Mode = 'Animated',
    [switch]$Apply, [switch]$InstallOnly, [switch]$Restore, [switch]$List
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'CursorStudio.Core.ps1')
$Root = Split-Path -Parent $PSScriptRoot          # CursorSets\ (holds catalog.json, Sets\, Previews\)
$catalog = Get-CursorCatalog -Root $Root

# ------------------------------------------------------------------ headless mode
if ($List -or $Set -or $Restore) {
    if ($List) {
        foreach ($s in $catalog.sets) { foreach ($st in $s.styles) { '{0,-34} {1,-3} {2}' -f $s.slug, $st.key, $st.label } }
        return
    }
    if ($Restore) { Restore-WindowsCursors; 'Restored the Windows default cursors.'; return }
    $pick = Get-CursorStyle -Catalog $catalog -Set $Set -Style $Style
    $res = Install-CursorSet -Root $Root -Catalog $catalog -Set $pick.Set -Style $pick.Style -Mode $Mode -Apply:($Apply -or -not $InstallOnly)
    "{0}: {1}" -f $(if ($res.Applied) { 'Applied' } else { 'Installed' }), $res.Label
    return
}

# ------------------------------------------------------------------------- GUI
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()

$cBg     = [Drawing.Color]::FromArgb(14, 17, 30)
$cPanel  = [Drawing.Color]::FromArgb(24, 28, 46)
$cPanel2 = [Drawing.Color]::FromArgb(36, 41, 66)
$cText   = [Drawing.Color]::FromArgb(234, 237, 251)
$cDim    = [Drawing.Color]::FromArgb(152, 162, 200)
$cAccent = [Drawing.Color]::FromArgb(70, 212, 255)
$cGood   = [Drawing.Color]::FromArgb(111, 227, 164)
$cBad    = [Drawing.Color]::FromArgb(255, 120, 130)
$font    = New-Object Drawing.Font('Segoe UI', 9.5)
$fontB   = New-Object Drawing.Font('Segoe UI Semibold', 10)
$fontH   = New-Object Drawing.Font('Segoe UI Semibold', 17)

function New-DarkButton([string]$text, [bool]$primary = $false) {
    $b = New-Object Windows.Forms.Button
    $b.Text = $text; $b.FlatStyle = 'Flat'; $b.Font = $fontB; $b.Height = 38
    $b.ForeColor = $(if ($primary) { [Drawing.Color]::FromArgb(6, 18, 26) } else { $cText }); $b.Cursor = [Windows.Forms.Cursors]::Hand
    $b.FlatAppearance.BorderSize = 1
    $b.FlatAppearance.BorderColor = $(if ($primary) { $cAccent } else { $cPanel2 })
    $b.BackColor = $(if ($primary) { $cAccent } else { $cPanel2 })
    $b.FlatAppearance.MouseOverBackColor = $(if ($primary) { [Drawing.Color]::FromArgb(130, 226, 255) } else { [Drawing.Color]::FromArgb(56, 62, 92) })
    $b
}
function New-DarkRadio([string]$text, [int]$x, [int]$y) {
    $r = New-Object Windows.Forms.RadioButton
    $r.Text = $text; $r.AutoSize = $true; $r.Location = New-Object Drawing.Point($x, $y); $r.Font = $fontB; $r.ForeColor = $cText
    $r
}

$form = New-Object Windows.Forms.Form
$form.Text = 'Cursor Studio'; $form.Size = New-Object Drawing.Size(1120, 760); $form.MinimumSize = New-Object Drawing.Size(1040, 700)
$form.StartPosition = 'CenterScreen'; $form.BackColor = $cBg; $form.ForeColor = $cText; $form.Font = $font

Add-Type -Namespace CursorStudio -Name Dwm -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("dwmapi.dll")]
public static extern int DwmSetWindowAttribute(System.IntPtr hwnd, int attr, ref int value, int size);
'@
$form.Add_HandleCreated({ $v = 1; [void][CursorStudio.Dwm]::DwmSetWindowAttribute($form.Handle, 20, [ref]$v, 4) })

$title = New-Object Windows.Forms.Label
$title.Text = 'Cursor Studio'; $title.Font = $fontH; $title.AutoSize = $true; $title.Location = New-Object Drawing.Point(20, 14)
$sub = New-Object Windows.Forms.Label
$sub.Text = '24 sets - 4 styles each (A relic, B mascot, C gauntlet/HUD/pixel, C2 extra) - 17 pointers - animated .ani or static .cur'
$sub.ForeColor = $cDim; $sub.AutoSize = $true; $sub.Location = New-Object Drawing.Point(22, 48)

$tree = New-Object Windows.Forms.TreeView
$tree.Location = New-Object Drawing.Point(20, 84); $tree.Size = New-Object Drawing.Size(300, 600)
$tree.Anchor = 'Top,Bottom,Left'; $tree.BackColor = $cPanel; $tree.ForeColor = $cText; $tree.BorderStyle = 'None'
$tree.ShowLines = $false; $tree.ItemHeight = 26; $tree.HideSelection = $false; $tree.DrawMode = 'OwnerDrawText'; $tree.FullRowSelect = $true; $tree.ShowRootLines = $false
$tree.Add_DrawNode({
    param($s, $e)
    $sel = ($e.State -band [Windows.Forms.TreeNodeStates]::Selected) -ne 0
    $bounds = New-Object Drawing.Rectangle(0, $e.Bounds.Y, $s.ClientSize.Width, $e.Bounds.Height)
    $e.Graphics.FillRectangle((New-Object Drawing.SolidBrush($(if ($sel) { $cAccent } else { $cPanel }))), $bounds)
    $isRoot = ($e.Node.Level -eq 0)
    $col = if ($sel) { [Drawing.Color]::FromArgb(6, 18, 26) } elseif ($isRoot) { $cDim } else { $cText }
    [Windows.Forms.TextRenderer]::DrawText($e.Graphics, $e.Node.Text, $(if ($isRoot) { $fontB } else { $font }), (New-Object Drawing.Point($(if ($isRoot) { 8 } else { 20 }), ($e.Bounds.Y + 4))), $col)
})
foreach ($g in ($catalog.sets | Group-Object group)) {
    $n = $tree.Nodes.Add($g.Name.ToUpper().Replace('-', ' / '))
    foreach ($s in $g.Group) { $c = $n.Nodes.Add(('{0:00}  {1}' -f [int]$s.num, ($s.name -replace '^[^-]+- ', ''))); $c.Tag = $s }
    $n.Expand()
}

$styleBox = New-Object Windows.Forms.Panel
$styleBox.Location = New-Object Drawing.Point(340, 84); $styleBox.Size = New-Object Drawing.Size(740, 34); $styleBox.Anchor = 'Top,Left,Right'
$rbStyle = @{}
$x = 0
foreach ($k in 'A', 'B', 'C', 'C2') { $r = New-DarkRadio "Style $k" $x 6; $rbStyle[$k] = $r; $styleBox.Controls.Add($r); $x += 110 }
$rbStyle['A'].Checked = $true

$lblStyle = New-Object Windows.Forms.Label
$lblStyle.Font = $fontB; $lblStyle.AutoSize = $false; $lblStyle.Size = New-Object Drawing.Size(740, 22)
$lblStyle.Location = New-Object Drawing.Point(340, 120); $lblStyle.Anchor = 'Top,Left,Right'
$lblBlurb = New-Object Windows.Forms.Label
$lblBlurb.ForeColor = $cDim; $lblBlurb.AutoSize = $false; $lblBlurb.Size = New-Object Drawing.Size(740, 22)
$lblBlurb.Location = New-Object Drawing.Point(340, 142); $lblBlurb.Anchor = 'Top,Left,Right'

$pic = New-Object Windows.Forms.PictureBox
$pic.Location = New-Object Drawing.Point(340, 170); $pic.Size = New-Object Drawing.Size(740, 384)
$pic.Anchor = 'Top,Left,Right'; $pic.BackColor = $cPanel; $pic.SizeMode = 'Zoom'

$modeBox = New-Object Windows.Forms.Panel
$modeBox.Location = New-Object Drawing.Point(340, 562); $modeBox.Size = New-Object Drawing.Size(740, 32); $modeBox.Anchor = 'Top,Left,Right'
$rbAnim = New-DarkRadio 'Animated (.ani)' 0 6; $rbAnim.Checked = $true
$rbStat = New-DarkRadio 'Static (.cur)' 170 6
$modeBox.Controls.AddRange(@($rbAnim, $rbStat))

$btnApply   = New-DarkButton 'Apply Now' $true
$btnInstall = New-DarkButton 'Add to Scheme List'
$btnRestore = New-DarkButton 'Restore Windows Default'
$btnMouse   = New-DarkButton 'Mouse Settings'
foreach ($b in @($btnApply, $btnInstall, $btnRestore, $btnMouse)) { $b.Anchor = 'Top,Left'; $form.Controls.Add($b) }
$btnApply.SetBounds(340, 600, 170, 40); $btnInstall.SetBounds(520, 600, 180, 40)
$btnRestore.SetBounds(710, 600, 210, 40); $btnMouse.SetBounds(930, 600, 150, 40)

$status = New-Object Windows.Forms.Label
$status.AutoSize = $false; $status.Size = New-Object Drawing.Size(740, 44); $status.Location = New-Object Drawing.Point(340, 648)
$status.Anchor = 'Top,Left,Right'; $status.ForeColor = $cDim
$status.Text = 'Pick a set, a style and Animated or Static, then press Apply Now. No administrator rights are needed.'

$form.Controls.AddRange(@($title, $sub, $tree, $styleBox, $lblStyle, $lblBlurb, $pic, $modeBox, $status))

$script:Current = $null
function Get-Mode { if ($rbAnim.Checked) { 'Animated' } else { 'Static' } }
function Get-StyleKey { foreach ($k in 'A', 'B', 'C', 'C2') { if ($rbStyle[$k].Checked) { return $k } } 'A' }
function Get-CurrentStyle { if (-not $script:Current) { return $null } $script:Current.styles | Where-Object { $_.key -eq (Get-StyleKey) } | Select-Object -First 1 }

function Show-Preview {
    $st = Get-CurrentStyle
    if (-not $st) { return }
    foreach ($k in 'A', 'B', 'C', 'C2') { $s2 = $script:Current.styles | Where-Object { $_.key -eq $k }; if ($s2) { $rbStyle[$k].Text = "$k  $($s2.label)" } }
    $file = if ((Get-Mode) -eq 'Animated') { 'board.gif' } else { 'board.png' }
    $p = Join-Path (Join-Path $Root $st.preview) $file
    if ($pic.Image) { $old = $pic.Image; $pic.Image = $null; $old.Dispose() }
    if (Test-Path -LiteralPath $p) { $pic.Image = [Drawing.Image]::FromStream((New-Object IO.MemoryStream(, [IO.File]::ReadAllBytes($p)))) }
    $lblStyle.Text = "$($script:Current.name)  -  Style $($st.key): $($st.label)"
    $lblBlurb.Text = $st.blurb
}
foreach ($k in 'A', 'B', 'C', 'C2') { $rbStyle[$k].Add_CheckedChanged({ if ($this.Checked) { Show-Preview } }) }
$rbAnim.Add_CheckedChanged({ Show-Preview })
foreach ($k in 'A', 'B', 'C', 'C2') { $rbStyle[$k].AutoSize = $false; $rbStyle[$k].Width = 180 }
$x = 0; foreach ($k in 'A', 'B', 'C', 'C2') { $rbStyle[$k].Left = $x; $x += 185 }
$tree.Add_AfterSelect({ if ($tree.SelectedNode -and $tree.SelectedNode.Tag) { $script:Current = $tree.SelectedNode.Tag; Show-Preview } })

function Invoke-Action([scriptblock]$work, [string]$okText) {
    try {
        $form.Cursor = [Windows.Forms.Cursors]::WaitCursor
        $res = & $work
        $status.ForeColor = $cGood; $status.Text = $okText.Replace('{0}', [string]$res)
    } catch {
        $status.ForeColor = $cBad; $status.Text = 'Failed: ' + $_.Exception.Message
    } finally { $form.Cursor = [Windows.Forms.Cursors]::Default }
}
function Test-Selection { if (-not $script:Current) { $status.ForeColor = $cBad; $status.Text = 'Select a cursor set first.'; return $false } $true }

$btnApply.Add_Click({
    if (Test-Selection) { Invoke-Action { (Install-CursorSet -Root $Root -Catalog $catalog -Set $script:Current -Style (Get-CurrentStyle) -Mode (Get-Mode) -Apply).Label } 'Applied: {0}. Move your mouse - the new pointers are live.' }
})
$btnInstall.Add_Click({
    if (Test-Selection) { Invoke-Action { (Install-CursorSet -Root $Root -Catalog $catalog -Set $script:Current -Style (Get-CurrentStyle) -Mode (Get-Mode)).Label } 'Added "{0}" to Mouse Settings > Pointers > Scheme.' }
})
$btnRestore.Add_Click({ Invoke-Action { Restore-WindowsCursors; 'Windows Default' } 'Restored: {0}.' })
$btnMouse.Add_Click({ Start-Process 'control.exe' -ArgumentList 'main.cpl,,1' })

$form.Add_Shown({ if ($tree.Nodes.Count -gt 0 -and $tree.Nodes[0].Nodes.Count -gt 0) { $tree.SelectedNode = $tree.Nodes[0].Nodes[0] } })
[void]$form.ShowDialog()
