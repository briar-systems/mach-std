Add-Type @'
using System;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;
public static class Volume607 {
    [StructLayout(LayoutKind.Sequential)]
    public struct IoStatus { public IntPtr Status; public UIntPtr Information; }
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    public static extern SafeFileHandle CreateFileW(string path, uint access, uint share, IntPtr security, uint creation, uint flags, IntPtr template);
    [DllImport("ntdll.dll")]
    public static extern int NtQueryVolumeInformationFile(SafeFileHandle handle, out IoStatus io, IntPtr data, uint size, uint kind);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool GetFileInformationByHandleEx(SafeFileHandle handle, uint kind, IntPtr data, uint size);
    public static string Probe(string path) {
        using (var handle = CreateFileW(path, 0x00010080, 7, IntPtr.Zero, 3, 0x02200000, IntPtr.Zero)) {
            if (handle.IsInvalid) throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
            IntPtr data = Marshal.AllocHGlobal(4096);
            try {
                IoStatus io;
                int status = NtQueryVolumeInformationFile(handle, out io, data, 4096, 5);
                if (status < 0) throw new Exception("attribute query status " + status.ToString("X8"));
                uint attributes = unchecked((uint)Marshal.ReadInt32(data));
                int maximum = Marshal.ReadInt32(data, 4);
                int nameBytes = Marshal.ReadInt32(data, 8);
                if (nameBytes < 0 || nameBytes > 4084 || (nameBytes & 1) != 0) throw new Exception("invalid returned name length");
                string name = Marshal.PtrToStringUni(IntPtr.Add(data, 12), nameBytes / 2);
                status = NtQueryVolumeInformationFile(handle, out io, data, 4096, 4);
                if (status < 0) throw new Exception("device query status " + status.ToString("X8"));
                uint characteristics = unchecked((uint)Marshal.ReadInt32(data, 4));
                string device = String.Format("device_status=0x{0:X8} device_bytes={1}", status, io.Information);
                status = NtQueryVolumeInformationFile(handle, out io, data, 16, 5);
                uint prefixAttributes = unchecked((uint)Marshal.ReadInt32(data));
                string prefix = String.Format("prefix_status=0x{0:X8} prefix_bytes={1} prefix_attributes=0x{2:X8}", status, io.Information, prefixAttributes);
                string protocol = "local";
                if ((characteristics & 0x10) != 0) {
                    for (int i = 0; i < 116; i++) Marshal.WriteByte(data, i, 0);
                    Marshal.WriteInt16(data, 0, 2);
                    Marshal.WriteInt16(data, 2, 116);
                    if (!GetFileInformationByHandleEx(handle, 13, data, 116)) throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
                    protocol = unchecked((uint)Marshal.ReadInt32(data, 4)).ToString("X8");
                }
                return String.Format("path={0} filesystem={1} attributes=0x{2:X8} posix={3} maximum={4} characteristics=0x{5:X8} remote={6} protocol={7} {8} {9}", path, name, attributes, (attributes & 0x400) != 0, maximum, characteristics, (characteristics & 0x10) != 0, protocol, prefix, device);
            } finally { Marshal.FreeHGlobal(data); }
        }
    }
}
'@
[Volume607]::Probe($env:GITHUB_WORKSPACE)
[Volume607]::Probe('\\localhost\MachStd607')
$ownedFile = Join-Path $env:GITHUB_WORKSPACE 'mach_607_capability_file'
[IO.File]::WriteAllText($ownedFile, 'probe')
try { [Volume607]::Probe('\\localhost\MachStd607\mach_607_capability_file') }
finally { [IO.File]::Delete($ownedFile) }
Get-SmbConnection | Format-List ServerName, ShareName, Dialect
