---
title: "Watson"
date: 2026-03-18T12:25:15+05:30
tags: ['Windows', 'Disk Analysis']
categories: ['for'] # for | crypto | osint | rev | pwn 
authors: ['pastimeplays']
description: ":))"
---

# Watson

<!-- DESCRIPTION -->
> We need your help again agent. The threat actor was able to escalate privileges. We're in the process of containment and we want you to find a few things on the threat actor. The triage is the same as the one in "Landfall". Can you read the briefing and solve your part of the case?

points: `385`

solves: `246`

handouts: [`Modified_KAPE_Triage_Files.zip`, `briefing.txt`, `how-to-solve.txt`, `checkpointA.zip`, `checkpointB.zip`]

author: `@jarpiano`

---

## Challenge Description

Once again - 

- `how-to-solve.txt`
```
To obtain the flag, you must pass through all of the checkpoints. The 
checkpoints have all been encrypted with a password. The password for each 
checkpoint can be found by answering the problems in the Briefing. After 
completing each checkpoint, you will be given a part of the flag. Combine the 
checkpoint hashes along with hyphens to obtain the flag. 

Example: utflag{DEAD-BEEF}
```

- `briefing.txt`
```
Welcome back agent. Please get us the following:

Checkpoint A: The threat actor deleted a word document containing secret 
project information. Can you retrieve it and submit the name of the project?

Checkpoint B: The threat actor installed a suspicious looking program that 
may or may not be benign. Retrieve the SHA1 Hash of the executable.

Hint: 
- Checkpoint A's password is strictly uppercase
- Checkpoint B's password is the SHA1 Hash
```

--- 

## Solution

### Checkpoint A - Deleted Word Document
This one's fairly simple. We know for a fact that the word document was deleted, so the logical first place to check would be the `$Recycle Bin` directory. 
```sh
$ cd '$Recycle.Bin'/
$ cd S-1-5-21-47857934-2514792372-2285641962-500/
$ ls
'$I07YGFU.docx'  '$IDYD79O'      '$IR5UOFV.txt'  '$R07YGFU.docx'  '$RDYD79O'      '$RR5UOFV.txt'
'$I9W158M.txt'   '$INJXINC.exe'  '$IZ7G627.exe'  '$R9W158M.txt'   '$RNJXINC.exe'  '$RZ7G627.exe'
```
The `$I` records contain metadata about a file while the `$R` contain the actual file contents. We can see that there is a single `.docx` file present here, so let's check what it has.

![Word SS]({6F735A0D-7E1F-4172-BDB6-B1811D082CBC}.png)
We've got our project name. 

### Checkpoint B - The Suspicious Program

The only thing we know as of now is that we're looking for a suspicious looking executable. Since we have no clue about where this is going to be present, it's gonna be hassle poking around for this.\
The good news is that when it comes to executables, there is a Windows Registry Hive File called `AmCache.hve`, that contains details on executables in a system. So let's check that out. It is present in
```sh
C/Windows/AppCompat/Programs/Amcache.hve
```
To parse through this data, I will be using one of [Zimmerman's tools](https://ericzimmerman.github.io/#!index.md), the AmcacheParser.
```powershell
>  .\AmcacheParser.exe -f .\Amcache.hve --csv "." --csvf "AmcacheOutput.csv"
AmcacheParser version 1.5.2.0

Author: Eric Zimmerman (saericzimmerman@gmail.com)
https://github.com/EricZimmerman/AmcacheParser

Command line: -f .\Amcache.hve --csv . --csvf AmcacheOutput.csv

Warning: Administrator privileges not found!

Two transaction logs found. Determining primary log...
Primary log: C:\Users\pasti\Desktop\CTF\ctf tools\AmcacheParser\Amcache.hve.LOG1, secondary log: C:\Users\pasti\Desktop\CTF\ctf tools\AmcacheParser\Amcache.hve.LOG2
Replaying log file: C:\Users\pasti\Desktop\CTF\ctf tools\AmcacheParser\Amcache.hve.LOG1
Replaying log file: C:\Users\pasti\Desktop\CTF\ctf tools\AmcacheParser\Amcache.hve.LOG2
At least one transaction log was applied. Sequence numbers have been updated to 0x0062. New Checksum: 0x233C11A3
Two transaction logs found. Determining primary log...
Primary log: C:\Users\pasti\Desktop\CTF\ctf tools\AmcacheParser\Amcache.hve.LOG1, secondary log: C:\Users\pasti\Desktop\CTF\ctf tools\AmcacheParser\Amcache.hve.LOG2
Replaying log file: C:\Users\pasti\Desktop\CTF\ctf tools\AmcacheParser\Amcache.hve.LOG1
Replaying log file: C:\Users\pasti\Desktop\CTF\ctf tools\AmcacheParser\Amcache.hve.LOG2
At least one transaction log was applied. Sequence numbers have been updated to 0x0062. New Checksum: 0x233C11A3

C:\Users\pasti\Desktop\CTF\ctf tools\AmcacheParser\Amcache.hve is in new format!

Total file entries found: 518
Total shortcuts found: 77
Total device containers found: 15
Total device PnPs found: 182
Total drive binaries found: 358
Total driver packages found: 1

Found 74 unassociated file entry

Results saved to: .

Total parsing time: 0.292 seconds
```
Out of the generated files, `AmcacheOutput_UnassociatedFileEntries.csv` is the one that will contain our required executable data.\
Reading through the first few lines shows us something interesting.

```
ApplicationName,ProgramId,FileKeyLastWriteTimestamp,SHA1,IsOsComponent,FullPath,Name,FileExtension,LinkDate,ProductName,Size,Version,ProductVersion,LongPathHash,BinaryType,IsPeFile,BinFileVersion,BinProductVersion,Usn,Language,Description
Unassociated,0006d9ae4e1a50b84d5a2616319a5188b6b700000000,2026-03-12 03:39:48,67198a3ca72c49fb263f4a9749b4b79c50510155,False,c:\users\administrator\appdata\local\ithqsu\2ga2pl\calc.exe,Calc.exe,.exe,2104-07-18 17:22:04,helloworld,4096,1.0.0.0,1.0.0.0,calc.exe|bb6d3e29a64aae32,pe64_clr_64,False,1.0.0.0,1.0.0.0,92693904,0,
Unassociated,0006889e71d0c13a020c6b25e4dd3d78ad6f00000000,2026-03-12 03:12:06,099050247e58084963bcc657b1f1699fde6f5df6,False,c:\users\administrator\appdata\local\calculator.exe,Calculator.exe,.exe,2019-08-02 21:50:49,microsoft calculator,4099584,10.1906.55.0,10.1906.55.0,calculator.exe|1d80f8116487329c,pe64_amd64,False,10.1906.55.0,10.1906.55.0,89942720,0,
Unassociated,0006e5e7dc869e1d801e09abb18aaa90713d00000904,2026-03-09 19:36:44,a615e68b956b5efc6be9a731db7af34ed0329af0,False,c:\users\jon\downloads\chromesetup.exe,ChromeSetup.exe,.exe,2026-02-25 04:02:30,google installer (x86),11476408,147.0.7703.0,147.0.7703.0,chromesetup.exe|86c9527b7e4ae18,pe32_i386,False,147.0.7703.0,147.0.7703.0,27311800,1033,
Unassociated,0006e5e7dc869e1d801e09abb18aaa90713d00000904,2026-03-09 21:37:28,dbf3e3f688eafe915793c202c92f62b3d287e2d3,False,c:\users\robb\downloads\chromesetup.exe,ChromeSetup.exe,.exe,2026-02-25 04:02:30,google installer (x86),11476408,147.0.7703.0,147.0.7703.0,chromesetup.exe|d86ef67b030d7ec9,pe32_i386,False,147.0.7703.0,147.0.7703.0,44813656,1033,
Unassociated,0000f519feec486de87ed73cb92d3cac802400000000,2026-03-09 19:36:21,92be78f815897d905538b36fbf015af29616cc49,True,c:\windows\system32\compattelrunner.exe,CompatTelRunner.exe,.exe,2025-09-21 17:11:14,microsoft® windows® operating system,185728,10.0.19645.1102 (winbuild.160101.0800),10.0.19645.1102,compattelrunner.|732ad1627e12cb48,pe64_amd64,False,10.0.19645.1102,10.0.19645.1102,0,1033,
```
We see a `Calc.exe` with a product name of `helloworld`. They think they sneaky with that. Amcache also provides us with a SHA1 hash for all the executables, so we use it to unlock the second checkpoint. 

--- 

```
utflag{pr1v473_3y3-m1551n6_l1nk}
```

