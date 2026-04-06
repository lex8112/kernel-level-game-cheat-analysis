rule Detect_Anti_Debug_Tricks {
    meta:
        author = "Reverse Engineer"
        description = "Detects common anti-debugging and kernel-level hooking patterns used by game protectors."
        date = "2026-04-07"
        version = "1.0"
        
    strings:
        // WinDbg veya x64dbg tespit etmeye çalışan API çağrıları
        $api1 = "IsDebuggerPresent" ascii wide
        $api2 = "CheckRemoteDebuggerPresent" ascii wide
        $api3 = "NtQueryInformationProcess" ascii wide
        
        // YDArk veya Process Hacker sürücülerini (driver) arayan patternler
        $driver1 = "\\\\.\\ProcessHacker" nocase wide
        $driver2 = "\\\\.\\YDArk" nocase wide
        
        // TODO: Add entropy calculation module for packed sections
        
    condition:
        uint16(0) == 0x5a4d and // PE File (MZ)
        (2 of ($api*) or any of ($driver*))
}
