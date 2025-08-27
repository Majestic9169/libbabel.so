---
title: "Secure-Server-2"
date: 2025-08-22T14:52:52+05:30
tags: ["AES","Wireshark"]
categories: ['crypto'] # for | cry | osint | rev | pwn 
authors: ['pastimeplays']
description: "Slight upgrade of the previous version"
---

# Secure Server 2

<!-- DESCRIPTION -->
> This time, the server is even more secure, but did it actually receive the secret? Simple brute-force won't work!

points: `432`

solves: `206`

handouts: [`capture.pcap`,`server.py`,`johndoe.py`]

author: `NoobMaster`

---

## Challenge Description

server.py contains - 
```python
import os
from Crypto.Cipher import AES
print("With the Secure Server 2, sharing secrets is safer than ever! We now support double encryption with AES!")
enc = bytes.fromhex(input("Enter the secret, encrypted twice with your keys (in hex): ").strip())
# Our proprietary key generation method, used by the server and John Doe himself!
k3 = b'BB' # Obviously not the actual key
k4 = b'B}' # Obviously not the actual key
# flag = secret_message + k1 + k2 + k3 + k4 (where each key is 2 bytes)
# In this case: scriptCTF{s3cr37_m3ss4g3_1337!_7e4b3f8d}
keys = [k3,k4]
final_keys = []
for key in keys:
    assert len(key) == 2 # 2 byte key into binary
    final_keys.append(bin(key[0])[2:].zfill(8)+bin(key[1])[2:].zfill(8))

cipher = AES.new(final_keys[0].encode(), mode=AES.MODE_ECB)
cipher2 = AES.new(final_keys[1].encode(), mode=AES.MODE_ECB)
enc2 = cipher2.encrypt(cipher.encrypt(enc)).hex()
print(f"Quadriple encrypted secret (in hex): {enc2}")
dec = bytes.fromhex(input("Decrypt the above with your keys again (in hex): ").strip())
secret = cipher.decrypt(cipher2.decrypt(dec))
print("Secret received!")
```
From the code what we get is that the server picks two keys (which are weak), double AES encrypts an input from John Doe and sends it back for him to decrypt with his keys.
It then double decrypts the next input from John to get the secret.

Next, from John Doe's code - 
```python
from Crypto.Cipher import AES
k1 = b'AA' # Obviously not the actual key
k2 = b'AA' # Obviously not the actual key
message = b'scriptCTF{testtesttesttesttest!_' # Obviously not the actual flag
keys = [k1,k2]
final_keys = []
for key in keys:
    assert len(key) == 2 # 2 byte key into binary
    final_keys.append(bin(key[0])[2:].zfill(8)+bin(key[1])[2:].zfill(8))


cipher = AES.new(final_keys[0].encode(), mode=AES.MODE_ECB)
cipher2 = AES.new(final_keys[1].encode(), mode=AES.MODE_ECB)
enc2 = cipher2.encrypt(cipher.encrypt(message)).hex()

print(enc2)

to_dec = bytes.fromhex(input("Dec: ").strip())

secret = cipher.decrypt(cipher2.decrypt(to_dec))

print(secret.hex())
```
We see that he does a similar thing, picking a secret, double encrypting it, sending it to the server and then double decrypting the server response


And finally, we have the network logs that capture this conversation  - 
```
S : With the Secure Server 2, sharing secrets is safer than ever! We now support double encryption with AES!
S : Enter the secret, encrypted twice with your keys (in hex): 
JD : 19574ac010cc9866e733adc616065e6c019d85dd0b46e5c2190c31209fc57727

S : Quadriple encrypted secret (in hex): 0239bcea627d0ff4285a9e114b660ec0e97f65042a8ad209c35a091319541837
S : Decrypt the above with your keys again (in hex): 
JD : 4b3d1613610143db984be05ef6f37b31790ad420d28e562ad105c7992882ff34

S : Secret received!
```

--- 

## Solution

There is an implementation issue here because unlike XOR, the order of encryptions and decryptions matter in AES. If the server encrypts AFTER John, it must decrypt BEFORE John, otherwise the resulting plaintext will be gibberish, you can try it out yourself in this problem if you want.

### Meet in the Middle Attack

The solution to this problem requires us to know the "Meet in the Middle" attack which is commonly used when there are multiple consecutive encryptions/decryptions. Let me explain it in simple words - 

Lets say that I have an encrpytion scheme that could give me ciphertexts with 100 possible keys, and I am encrypting a plaintext by using this cipher twice on it (with different keys $k_1$, $k_2$). I have access to both the plaintext and the ciphertext but not the intermediate value possessed after only one stage. My job is to find the keys used.

Now one way I could go about it is to go through every combination of the keys $k_1$ and $k_2$ and manually double encrypt the plaintext with each combination. This would lead me to go through at worst every simble combination ($100*100 = 10000$ possibilities)

Now let's think of a separate approach. I encrypt the plaintext with ever possible key once ($100$ times) and store all the possible intermediate values in a lookup table. Then, we decrypt the ciphertext with every possible key once ($100$ times). Now because the intermediate value should exist in both the tables, I only need to look for a match, which makes my worst case only $200$ operations as opposed to the first method's $10000$ operations.

This might not seem like much of a difference but that is because I've taken the example of $100$ possibilities, real life cases have much bigger numbers involved.

### Getting the server keys

We can begin by getting the server keys. Now according to the code provided, $k4$ depends on only $1$ unknown byte and $k3$ depends on $2$ unknowns bytes. We also know the plaintext and ciphertext involved for this encryption. So we first store the possible intermediate values by decrypting ciphertext with $k4$ and compare them with values encountered while encrypting plaintext with $k3$.
```python
from Crypto.Cipher import AES 

ct = bytes.fromhex("0239bcea627d0ff4285a9e114b660ec0e97f65042a8ad209c35a091319541837")
pt = bytes.fromhex("19574ac010cc9866e733adc616065e6c019d85dd0b46e5c2190c31209fc57727")

lookup = {}

for k4 in range(256):
    key4 = bytes.fromhex(f"{k4:02x}") + b'}'
    key = bin(key4[0])[2:].zfill(8)+bin(key4[1])[2:].zfill(8)
    cipher2 =  AES.new(key.encode(), mode=AES.MODE_ECB)
    lookup[cipher2.decrypt(ct)] = key4
    
candidates = lookup.keys()    

for k3 in range(256**2):
    key3 = bytes.fromhex(f"{k3:04x}")
    key = bin(key3[0])[2:].zfill(8)+bin(key3[1])[2:].zfill(8)
    cipher1 =  AES.new(key.encode(), mode=AES.MODE_ECB)
    
    wanted = (cipher1.encrypt(pt))
    
    if wanted in candidates:
        print(key3 + lookup[wanted])
        exit(0)
```

This gives us $k3$ + $k4$ as - ```b'f8d}'```

### Getting John's keys

The approach is pretty much the same here, the only change is the plaintext value and the fact that $k2$ also depends on 2 unknown bytes. 
```python
pt = bytes.fromhex("4b3d1613610143db984be05ef6f37b31790ad420d28e562ad105c7992882ff34")
for k2 in range(256**2):
    key2 = bytes.fromhex(f"{k2:04x}")
    .
    .
    .
```

This returns $k1$ + $k2$ - ```b'e4b3'```

### Retrieving original message

Now, with John's keys, we can just decrypt the original message to get the first part of the flag

```python
ct = bytes.fromhex("19574ac010cc9866e733adc616065e6c019d85dd0b46e5c2190c31209fc57727")

key1 = b'e4'
key2 = b'b3'
key = bin(key1[0])[2:].zfill(8)+bin(key1[1])[2:].zfill(8)
cipher1 =  AES.new(key.encode(), mode=AES.MODE_ECB)
key = bin(key2[0])[2:].zfill(8)+bin(key2[1])[2:].zfill(8)
cipher2 =  AES.new(key.encode(), mode=AES.MODE_ECB)
print(cipher1.decrypt(cipher2.decrypt(ct)))
```

which gives - ```b'scriptCTF{s3cr37_m3ss4g3_1337!_7'```

--- 

```
scriptCTF{s3cr37_m3ss4g3_1337!_7e4b3f8d}
```

