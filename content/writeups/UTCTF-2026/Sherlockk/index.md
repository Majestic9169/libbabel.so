---
title: "Sherlockk"
date: 2026-03-18T12:25:15+05:30
tags: ['Windows', 'Disk Analysis']
categories: ['for'] # for | crypto | osint | rev | pwn 
authors: ['pastimeplays']
description: "I feel smart"
---

# Sherlockk

<!-- DESCRIPTION -->
> We're almost done agent. All we need to do now is identify some Indicators of Compromise (IOCs) left by the threat actor, among other things. The triage is the same as the one in "Landfall" and "Watson". Can you read the briefing and solve your part of the case?

points: `490`

solves: `222`

handouts: [`Modified_KAPE_Triage_Files.zip`, `briefing.txt`, `how-to-solve.txt`, `checkpointA.zip`, `checkpointB.zip`, `checkpointC.zip`]

author: `@jarpiano`

---

## Challenge Description

No `how-to-solve.txt` for this one :(

- `briefing.txt`
```
Welcome back agent. Please get us the following:

Checkpoint A: The threat actor downloaded a file from a online text storage 
site. Can you identify the complete URL the threat actor downloaded from?

Checkpoint B: The threat actor wrote a note for himself on the machine. 
It's been deleted now, but can you retrieve the contents of the note?

Checkpoint C: The threat actor downloaded a file enumeration script. 
Can you submit the MD5 Hash of that file?

Hints:
- Checkpoint B's password consist of the listed items separated by a hyphens 
(e.g. Dead-Beef-Code)
```

I'll assume that the construction of the flag is the same as in [Watson](../Watson/). 

--- 

## Solution

### Checkpoint A - Browser History
Online text storage site? ONLINE? We check browser. Done. That's it. I picked the admin account here because that's where an attacker would be working, but you could go through every account if you want.
```sh
C/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default/History
```
Searching for the phrase `https` inside this leads us to our result - 
```sh
$ strings History | grep https
https://pastes.io/Pastes.io - Best Pastebin alternative
https://pastes.io/download/nhy8LSzI'
https://pastes.io/
```
### Checkpoint B - .txt Retrieval
Looking at the description, it bears some similarity to the deleted .docx file, so I check the `$Recycle Bin` directory first. Unfortunately, out of the two text files there, none of them serve our purpose. \
This is where we use our MFT file. Since the MFT is not human readable, I'll be using [Zimmerman's MFTECmd](https://ericzimmerman.github.io/#!index.md) to parse it.
```powershell
> .\MFTECmd.exe -f ".\`$MFT" --csv .\Output\ --csvf "RightOutput.csv" --ir
MFTECmd version 1.3.0.0

Author: Eric Zimmerman (saericzimmerman@gmail.com)
https://github.com/EricZimmerman/MFTECmd

Command line: -f .\$MFT --csv .\Output\ --csvf RightOutput.csv --ir

Warning: Administrator privileges not found!

File type: Mft

Processed .\$MFT in 1.7403 seconds

.\$MFT: FILE records found: 1,81,496 (Free records: 0) File size: 177.2MB
        CSV output will be saved to .\Output\RightOutput.csv
```
I now have the entire MFT data in the CSV format. As I mentioned in the [Landfall writeup](../Landfall/), if the contents of the file are small enough, they'll be present in the "Resident Data" entry of the MFT (which is why i included the `--ir` flag). \
Let's parse through all the `.txt` entries in the MFT. I also know that since this is likely to be short, the answer might be in the "Resident Data" of the entry, so I filter out all text files that don't have resident data.\
Reading through the remaining data led me to an interesting entry
```
160984,7,True,133573,3,.\Users\Administrator\Documents,Administrator Notes.txt,.txt,46,1,,False,False,False,False,False,False,Archive,Windows,2026-03-12 02:43:47.6878255,,2026-03-12 02:44:23.3591827,,2026-03-12 04:00:50.2084497,2026-03-12 02:44:23.3591827,2026-03-12 04:00:50.2861227,2026-03-12 02:44:23.3591827,95270928,960283337,2625,6754cfe9-1dbc-11f1-af31-000c29d1deaf,,,.\$MFT,R3JvY2VyeSBMaXN0Og0KLSBMZXR0dWNlDQotIENhYmJhZ2UNCi0gQ2Fycm90cw==,47-72-6F-63-65-72-79-20-4C-69-73-74-3A-0D-0A-2D-20-4C-65-74-74-75-63-65-0D-0A-2D-20-43-61-62-62-61-67-65-0D-0A-2D-20-43-61-72-72-6F-74-73,"Grocery List:
- Lettuce
- Cabbage
- Carrots"
```
This fits the format mentioned in the briefing!


### Checkpoint C - Downloads

I got lucky with this one since I stumbled upon it while solving Watson. This was a pretty basic one compared to the other parts of this challenge. The downloaded script is just sitting in the `Downloads` directory of the admin!
```sh
$ ls Users/Administrator/Downloads/
script.sh.sh

$ cd Users/Administrator/Downloads/

$ md5sum script.sh.sh
e86475121f231c02c4a63bd0915b9dff  script.sh.sh
```


--- 

```
utflag{b45k3rv1ll3-3l3m3n74ry-4r7hur_c0n4n_d0yl3}
```

