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
    public static string Probe(string path) {
        using (var handle = CreateFileW(path, 0, 7, IntPtr.Zero, 3, 0x02000000, IntPtr.Zero)) {
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
                return String.Format("path={0} filesystem={1} attributes=0x{2:X8} posix={3} maximum={4} characteristics=0x{5:X8} remote={6}", path, name, attributes, (attributes & 0x400) != 0, maximum, characteristics, (characteristics & 0x10) != 0);
            } finally { Marshal.FreeHGlobal(data); }
        }
    }
}
'@
[Volume607]::Probe($env:GITHUB_WORKSPACE)
[Volume607]::Probe('\\localhost\MachStd607')
Get-SmbConnection | Format-List ServerName, ShareName, Dialect
