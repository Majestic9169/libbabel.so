---
title: "Secure-Server"
date: 2025-08-21T10:25:35+05:30
tags: ["XORing","Wireshark"]
categories: ["crypto"] # for | cry | osint | rev | pwn 
authors: ["pastimeplays"]
description: " "
---

# Secure Server

<!-- DESCRIPTION -->
> John Doe uses this secure server where plaintext is never shared. Our Forensics Analyst was able to capture this traffic and the source code for the server. Can you recover John Doe's secrets?

points: `100`

solves: `541`

handouts: [`capture.pcap`,`server.py`]

author: `NoobMaster`

---

## Challenge Description

This was a basic communication eavesdropping challenge. Sounds fancy, but it basically means you have access to a conversation (which was given as a network capture file), and you need to figure out what was shared.

The communication from the side of the server is as follows (`server.py`) - 
```python
import os
from pwn import xor
print("With the Secure Server, sharing secrets is safer than ever!")
enc = bytes.fromhex(input("Enter the secret, XORed by your key (in hex): ").strip())
key = os.urandom(32)
enc2 = xor(enc,key).hex()
print(f"Double encrypted secret (in hex): {enc2}")
dec = bytes.fromhex(input("XOR the above with your key again (in hex): ").strip())
secret = xor(dec,key)
print("Secret received!")
```

The actual exchange can be found in the `capture.pcap` file as follows - 

```
S : With the Secure Server, sharing secrets is safer than ever!
S : Enter the secret, XORed by your key (in hex): 
JD : 151e71ce4addf692d5bac83bb87911a20c39b71da3fa5e7ff05a2b2b0a83ba03

S : Double encrypted secret (in hex): e1930164280e44386b389f7e3bc02b707188ea70d9617e3ced989f15d8a10d70
S : XOR the above with your key again (in hex): 
JD : 87ee02c312a7f1fef8f92f75f1e60ba122df321925e8132068b0871ff303960e

S : Secret received!
```
--- 

## Solution

From the server side communication we understand that - 

- $enc = plaintext  \oplus  key_1$ 
- $enc_2 = plaintext  \oplus  key_1 \oplus key_2$ 
- $dec = plaintext  \oplus  key_2$   
where $key_1$ is John Doe's key and $key_2$ is the server key (XORing with the same key twice cancels it out)

So what we need is the plaintext which can simply be obtained by XORing $enc$, $enc_2$ and $dec$ together

```python
enc = 0x151e71ce4addf692d5bac83bb87911a20c39b71da3fa5e7ff05a2b2b0a83ba03
enc2 = 0xe1930164280e44386b389f7e3bc02b707188ea70d9617e3ced989f15d8a10d70
dec = 0x87ee02c312a7f1fef8f92f75f1e60ba122df321925e8132068b0871ff303960e
print(bytes.fromhex(hex(enc^enc2^dec)[2:]))
```
--- 

```
scriptCTF{x0r_1s_not_s3cur3!!!!}
```

