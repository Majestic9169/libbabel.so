---
title: "RSA-1"
date: 2025-08-21T10:25:35+05:30
tags: ["XORing"]
categories: ["crypto"] # for | cry | osint | rev | pwn 
authors: ["pastimeplays"]
description: " "
---

# RSA 1

<!-- DESCRIPTION -->
> Yú Tóngyī send a message to 3 peoples with unique modulus. But he left it vulnerable. Figure out :)

points: `100`

solves: `696`

handouts: [`out.txt`]

author: `noob-abhinav`

---

## Challenge Description

We are given a text file containting some numbers - 
```
n1 = 156503881374173899106040027210320626006530930815116631795516553916547375688556673985142242828597628615920973708595994675661662789752600109906259326160805121029243681236938272723595463141696217880136400102526509149966767717309801293569923237158596968679754520209177602882862180528522927242280121868961697240587
c1 = 77845730447898247683281609913423107803974192483879771538601656664815266655476695261695401337124553851404038028413156487834500306455909128563474382527072827288203275942719998719612346322196694263967769165807133288612193509523277795556658877046100866328789163922952483990512216199556692553605487824176112568965

n2 = 81176790394812943895417667822424503891538103661290067749746811244149927293880771403600643202454602366489650358459283710738177024118857784526124643798095463427793912529729517724613501628957072457149015941596656959113353794192041220905793823162933257702459236541137457227898063370534472564804125139395000655909
c2 = 40787486105407063933087059717827107329565540104154871338902977389136976706405321232356479461501507502072366720712449240185342528262578445532244098369654742284814175079411915848114327880144883620517336793165329893295685773515696260299308407612535992098605156822281687718904414533480149775329948085800726089284

n3 = 140612513823906625290578950857303904693579488575072876654320011261621692347864140784716666929156719735696270348892475443744858844360080415632704363751274666498790051438616664967359811895773995052063222050631573888071188619609300034534118393135291537302821893141204544943440866238800133993600817014789308510399
c3 = 100744134973371882529524399965586539315832009564780881084353677824875367744381226140488591354751113977457961062275480984708865578896869353244823264759044617432862876208706282555040444253921290103354489356742706959370396360754029015494871561563778937571686573716714202098622688982817598258563381656498389039630

e = 3
```

The name makes it evident that this is an RSA challenge, and the description makes it safe to assume that the same message is being encrypted in all 3 cases

--- 

## Solution

### Recovering a larger C

This solution relies on a direct implementation of Chinese Remainder Theorem.

Given relations - 
$$m = c_1(mod\ n_1)$$
$$m = c_2(mod\ n_2)$$
$$\vdots$$
$$m = c_x(mod\ n_x)$$

We can find the value of $m$ modulo $n_1*n_2\cdots*n_x$ as long as $n_1,n_2\cdots,n_x$ are pairwise coprime
$$ m = c_1N_1N_1^{-1}+c_2N_2N_2^{-1}\cdots+c_xN_xN_x^{-1}\ (mod\ N) = c\ (mod\ N)$$
where - 

- $N = n_1*n_2\cdots*n_x$
- $N_i = \frac{B}{n_i}$
- $N_i^{-1} = N_i^{-1}\ (mod\ n_i)$

In our question, we have $x=3$, and using the above equation, we get a direct value of the ciphertext and modulus (the new modulus is the product of all the old moduli)

```python
N = n1*n2*n3
x1 = N//n1
x2 = N//n2
x3 = N//n3

m = (c1*x1*pow(x1,-1,n1) + c2*x2*pow(x2,-1,n2) + c3*x3*pow(x3,-1,n3))%N
```

### Recovering the message

Now the whole point of going through the trouble of getting a much larger ($c,N$) pair was the observation that our public exponent value is only 3! This means that if my modulus is large enough, even the cube of my message will remain unchanged after applying the modulo operation, and now we have a modulus 3 times the original given ones.

This means that we can most likely just take the cube root of the current number and that should give us the message - 
```python
from Crypto.Util.number import *

def crt(a):                     # Custom cube root cos math library cant handle these sizes :( 
    high = 1
    while high**3 <= a:         # Set upper limit for binary search
        high *= 2
        low = high//2
        mid = 0 
    while low < high:           # aaand binary search for cube root
        mid = (low+high+1)//2
        if mid**3 <= a:
            low = mid
        else:
            high = mid-1
    return mid

print(long_to_bytes(crt(m)))
```
--- 

```
scriptCTF{y0u_f0und_mr_yu's_s3cr3t_m3g_12a4e4}
```

