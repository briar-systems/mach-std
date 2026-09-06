$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory readonly-evidence | Out-Null
Start-Transcript -Path readonly-evidence/probe.txt
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class ForceDelete {
  [StructLayout(LayoutKind.Sequential)] public struct IOSB { public IntPtr Status; public UIntPtr Information; }
  [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
  public static extern IntPtr CreateFileW(string name, uint access, uint share, IntPtr security, uint disposition, uint flags, IntPtr template);
  [DllImport("kernel32.dll", SetLastError=true)] public static extern bool CloseHandle(IntPtr handle);
  [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)] public static extern bool CreateHardLinkW(string name, string existing, IntPtr security);
  [DllImport("ntdll.dll")] public static extern int NtSetInformationFile(IntPtr file, out IOSB iosb, IntPtr data, uint length, uint informationClass);
  [DllImport("ntdll.dll")] public static extern uint RtlNtStatusToDosError(int status);
  public static int Set(IntPtr handle, uint flags, bool basic) {
    IntPtr p = Marshal.AllocHGlobal(4);
    try { Marshal.WriteInt32(p, unchecked((int)flags)); IOSB io; return NtSetInformationFile(handle, out io, p, basic ? 1u : 4u, basic ? 13u : 64u); }
    finally { Marshal.FreeHGlobal(p); }
  }
}
'@
$fixture = Join-Path $env:RUNNER_TEMP ('readonly613-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory $fixture | Out-Null
$shareName = 'mach613' + [Guid]::NewGuid().ToString('N')
$shareCreated = $false
try {
  $user = [Security.Principal.WindowsIdentity]::GetCurrent().Name
  New-SmbShare -Name $shareName -Path $fixture -FullAccess $user | Out-Null
  $shareCreated = $true
  foreach ($backend in @('local', 'smb')) {
    $base = if ($backend -eq 'local') { $fixture } else { "\\localhost\$shareName" }
    foreach ($readonly in @($false, $true)) {
      foreach ($held in @($false, $true)) {
        foreach ($flags in @(1, 17, 19)) {
          $label = "$backend-ro$readonly-held$held-flags$flags"
          $file = Join-Path $base ($label + '.txt')
          $alias = Join-Path $base ($label + '-alias.txt')
          [IO.File]::WriteAllText($file, 'kept bytes')
          if (-not [ForceDelete]::CreateHardLinkW($alias, $file, [IntPtr]::Zero)) { throw "hardlink setup failed $label error=$([Runtime.InteropServices.Marshal]::GetLastWin32Error())" }
          if ($readonly) { [IO.File]::SetAttributes($file, [IO.FileAttributes]::ReadOnly -bor [IO.FileAttributes]::Archive) }
          $attributesBefore = [IO.File]::GetAttributes($alias)
          $reader = [IntPtr]::Zero
          if ($held) {
            $reader = [ForceDelete]::CreateFileW($file, 0x80000000, 7, [IntPtr]::Zero, 3, 0x02200000, [IntPtr]::Zero)
            if ($reader -eq [IntPtr](-1)) { throw "held setup failed $label" }
          }
          $handle = [ForceDelete]::CreateFileW($file, 0x00110080, 7, [IntPtr]::Zero, 3, 0x02200000, [IntPtr]::Zero)
          if ($handle -eq [IntPtr](-1)) { throw "delete open failed $label error=$([Runtime.InteropServices.Marshal]::GetLastWin32Error())" }
          try { $status = [ForceDelete]::Set($handle, [uint32]$flags, $flags -eq 1) }
          finally { if (-not [ForceDelete]::CloseHandle($handle)) { throw 'delete handle close failed' } }
          $existsWhileHeld = [IO.File]::Exists($file)
          if ($reader -ne [IntPtr]::Zero) { if (-not [ForceDelete]::CloseHandle($reader)) { throw 'reader close failed' } }
          $existsAfterClose = [IO.File]::Exists($file)
          $attributesAfter = [IO.File]::GetAttributes($alias)
          if ($attributesBefore -ne $attributesAfter -or [IO.File]::ReadAllText($alias) -ne 'kept bytes') { throw "alias mutated $label" }
          "$label status=$status win32=$([ForceDelete]::RtlNtStatusToDosError($status)) existsWhileHeld=$existsWhileHeld existsAfterClose=$existsAfterClose aliasUnchanged=True"
          if ($status -ge 0 -and $existsAfterClose) { throw "successful deletion retained pathname $label" }
          if ($status -lt 0 -and -not $existsAfterClose) { throw "failed deletion removed pathname $label" }
        }
      }
    }
  }
} finally {
  if ($shareCreated) { Remove-SmbShare -Name $shareName -Force }
  Remove-Item -LiteralPath $fixture -Recurse -Force
  Stop-Transcript
}
