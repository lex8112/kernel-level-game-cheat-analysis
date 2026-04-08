# Fileless Ring-0 Game Cheat — Technical Architecture

## Overview

This document describes the internal architecture of a fileless kernel-level game cheat that was reverse-engineered and analyzed in this project. The cheat uses a sophisticated multi-stage attack chain to inject code directly into kernel memory without leaving any artifacts on disk.

---

## Attack Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     USER MODE (Ring-3)                       │
│                                                             │
│  ┌──────────┐     ┌──────────────┐     ┌────────────────┐   │
│  │ cheat.exe │────▶│ Exploit SDK  │────▶│ Vulnerable     │   │
│  │ (loader)  │     │ (IOCTL call) │     │ Signed Driver  │   │
│  └──────────┘     └──────────────┘     │ (e.g. .sys)    │   │
│       │                                 └───────┬────────┘   │
│       │                                         │ DeviceIoControl()
├───────┼─────────────────────────────────────────┼───────────┤
│       │           KERNEL MODE (Ring-0)          │            │
│       │                                         ▼            │
│       │            ┌───────────────────────────────┐         │
│       │            │   Driver Vulnerability        │         │
│       │            │   (Arbitrary R/W Primitive)   │         │
│       │            └──────────┬────────────────────┘         │
│       │                       │                              │
│       │          ┌────────────▼────────────┐                 │
│       │          │  Non-Paged Pool Memory  │                 │
│       │          │  (ExAllocatePoolWith*)  │                 │
│       │          │                         │                 │
│       │          │  ┌───────────────────┐  │                 │
│       │          │  │ Injected Payload  │  │                 │
│       │          │  │ (Cheat Logic)     │  │                 │
│       │          │  │ • Memory R/W      │  │                 │
│       │          │  │ • SpinLock Sync   │  │                 │
│       │          │  │ • Thread Mgmt     │  │                 │
│       │          │  └────────┬──────────┘  │                 │
│       │          └───────────┼─────────────┘                 │
│       │                      │                               │
│       │     ┌────────────────▼─────────────────┐             │
│       │     │     nt!PsCreateSystemThread()    │             │
│       │     │     (Fake System Thread)         │             │
│       │     └────────────────┬─────────────────┘             │
│       │                      │                               │
├───────┼──────────────────────┼───────────────────────────────┤
│       │     UI INJECTION     │                               │
│       │                      ▼                               │
│       │        ┌──────────────────────┐                      │
│       │        │    dwm.exe           │                      │
│       └───────▶│  (Desktop Window     │                      │
│                │   Manager)           │                      │
│                │  • UI Overlay        │                      │
│                │  • Handle Stripped   │                      │
│                └──────────────────────┘                      │
│                                                              │
│                    USER MODE (Ring-3)                         │
└──────────────────────────────────────────────────────────────┘
```

---

## Stage-by-Stage Breakdown

### Stage 1: User-Mode Loader

| Property       | Detail                                           |
|----------------|--------------------------------------------------|
| **Binary**     | `cheat.exe` (polymorphic — name randomizes on download) |
| **Self-Defense** | Cannot be killed via Task Manager               |
| **Kill Switch** | Forces BSOD on termination attempt              |

The loader is a small user-mode executable. It does **not** contain the cheat logic itself — it only serves as a bootstrapper to exploit a vulnerable signed driver and transfer execution to Ring-0.

### Stage 2: Vulnerable Driver Exploitation

```
User Mode                    Kernel Mode
┌──────────┐   IOCTL    ┌────────────────────┐
│ cheat.exe │──────────▶│ Signed Driver (.sys)│
│           │           │ (legit vendor)      │
└──────────┘           │                    │
                        │ ┌────────────────┐ │
                        │ │ Bug: Arbitrary │ │
                        │ │ Memory R/W     │ │
                        │ │ via IOCTL      │ │
                        │ └────────────────┘ │
                        └────────────────────┘
```

- The cheat **does not bring its own driver** — no .sys file is written to disk
- Instead, it exploits a **legitimately signed third-party driver** (e.g., from Nvidia, Intel, or similar vendors)
- The vulnerability grants **arbitrary kernel memory read/write** primitives
- This technique bypasses Windows Driver Signature Enforcement entirely

### Stage 3: Kernel Memory Injection (Non-Paged Pool)

```c
// Conceptual representation of the injection technique
ExAllocatePoolWithTag(NonPagedPool, payload_size, 'CHEAT');
RtlCopyMemory(pool_address, shellcode, payload_size);
```

| Property          | Detail                                                   |
|-------------------|----------------------------------------------------------|
| **Memory Type**   | Non-Paged Pool (kernel memory that never swaps to disk)  |
| **Disk Footprint**| **Zero** — code exists only in volatile RAM              |
| **Module Registration** | None — code is not registered as a loaded module   |
| **Detection**     | Invisible to ProcMon, Process Hacker, YDArk              |

### Stage 4: Fake System Thread Creation

```c
// The cheat creates threads that appear as legitimate system threads
PsCreateSystemThread(&hThread, THREAD_ALL_ACCESS, NULL, NULL, NULL, CheatPayload, NULL);
```

- Threads are created via the kernel process manager (`nt!ps`)
- They appear as **System process threads** (PID 4)
- No associated module name — threads point to anonymous memory
- Invisible in standard process inspection tools

### Stage 5: DWM.exe Process Hijacking

```
┌─────────────────────────────────────┐
│           dwm.exe (PID: ...)        │
│  ┌───────────────────────────────┐  │
│  │ Legitimate DWM Rendering     │  │
│  │ (Windows Desktop Compositor) │  │
│  ├───────────────────────────────┤  │
│  │ INJECTED: Cheat UI Overlay   │◄─── Kernel-level injection
│  │ ■ ESP/Wallhack rendering     │  │
│  │ ■ Aimbot crosshair overlay   │  │
│  └───────────────────────────────┘  │
│                                     │
│  Handle Rights: STRIPPED            │
│  (ReadProcessMemory → ACCESS DENIED)│
└─────────────────────────────────────┘
```

- The cheat injects its visual overlay into **DWM.exe** (Desktop Window Manager)
- DWM is a **protected system process** — it renders all desktop windows
- The cheat **strips handle rights** (`ObRegisterCallbacks`) so no user-mode tool can read DWM's memory
- This makes the cheat's UI layer completely invisible to memory inspection

### Stage 6: Spin Lock Synchronization & BSOD Trigger

```
Thread A (Reader)              Thread B (Writer)
┌───────────────┐              ┌───────────────┐
│ Read game     │◄── SpinLock ──▶│ Write to UI  │
│ memory values │    (IRQL≥2)   │ overlay      │
└───────┬───────┘              └───────────────┘
        │
        │ On cheat close:
        │ Code memory is freed
        │ BUT Thread B still holds SpinLock
        │
        ▼
  ╔═══════════════════╗
  ║  BSOD: 0x1E       ║
  ║  KMODE_EXCEPTION   ║
  ║  NOT_HANDLED       ║
  ║                    ║
  ║  P1: 0xc0000005   ║ ← Access Violation
  ║  P2: NO MODULE    ║ ← Anonymous memory
  ╚═══════════════════╝
```

---

## Why Standard Tools Failed

| Tool            | What It Checks                        | Why It Failed                                        |
|-----------------|---------------------------------------|------------------------------------------------------|
| **ProcMon**     | File system writes (.sys creation)    | No file was ever written to disk                     |
| **Process Hacker** | Process list, services, drivers    | Cheat runs as System threads, not a process          |
| **YDArk**       | Kernel callbacks, hooks, hidden modules | No hooks installed — code runs from raw memory pool |
| **TCPView**     | Network connections (C2 traffic)      | No network activity — everything is local            |
| **WinDbg**      | Post-mortem crash analysis            | ✅ **Succeeded** — revealed anonymous kernel code    |

---

## Key Forensic Evidence (WinDbg)

```
BugCheck 1E (KMODE_EXCEPTION_NOT_HANDLED)
  Parameter 1: ffffffffc0000005  → Access Violation
  Parameter 2: ffffcc0e95e11225  → Crash address (NO MODULE NAME)
  Parameter 3: 0000000000000001
  Parameter 4: 000002253ad40008
```

The **absence of a module name** at the crash address is the definitive proof of fileless kernel injection. In a normal crash, WinDbg always resolves the faulting address to a loaded driver module. Here, the code exists only in **unregistered, anonymous Non-Paged Pool memory**.

---

## Defense: Why Ring-0 Anti-Cheat is Necessary

```
Traditional (Ring-3) Anti-Cheat:
  ✗ Cannot see kernel memory
  ✗ Cannot detect fileless payloads
  ✗ Can be bypassed via handle stripping
  ✗ Relies on disk scanning (.sys files)

Kernel (Ring-0) Anti-Cheat (e.g., Vanguard):
  ✓ Runs at same privilege level as cheat
  ✓ Can inspect Non-Paged Pool allocations
  ✓ Can detect unmarked system threads
  ✓ Can monitor kernel callbacks in real-time
```

---

## Repository Analysis Toolchain

| File                          | Purpose                                              |
|-------------------------------|------------------------------------------------------|
| `scripts/memory_scanner.py`   | Windows API-based memory reader using `ReadProcessMemory` |
| `scripts/procmon_analyzer.py` | ProcMon CSV log parser for suspicious registry/network events |
| `scripts/injection_poc.cpp`   | PoC demonstrating `VirtualAllocEx` + `CreateRemoteThread` |
| `yara/anti_debug_detect.yar`  | YARA rule detecting anti-debug API patterns & tool drivers |
| `docs/timeline.html`          | Interactive forensic investigation timeline (EN/TR)  |

---

*İstinye University — Reverse Engineering Course — Advisor: Keyvan Arasteh*
