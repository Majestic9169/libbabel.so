---
title: "Smooth Criminal"
date: 2026-03-15T22:58:02+05:30
tags: ['beginner']
categories: ['crypto'] # for | crypto | osint | rev | pwn 
authors: ['pastimeplays']
description: "I like the theory behind this one"
---

# Smooth Criminal

<!-- DESCRIPTION -->
> Our cryptographer assured us that a 649-bit prime makes this completely unbreakable. He also said the order of the group "doesn't really matter that much." He no longer works here.

points: `100`

solves: `496`

handouts: [`dlp.txt`]

author: `@GarvK07`

---

## Challenge Description
This challenge is built upon the Discrete Logarithm Problem (DLP). For those of you new to it, it is the problem of finding an $a$ given $g,h,p$ where 
$$g^a \equiv h\ (mod\ p)$$
(there's more to it, but that's the basic idea)

```
The flag has been encoded as a secret exponent x, where:

  h = g^x mod p

Your job: find x. Convert it from integer to bytes to get the flag.

p = 1363402168895933073124331075716158793413739602475544713040662303260999503992311247861095036060712607168809958344896622485452229880797791800555191761456659256252204001928525518751268009081850267001
g = 223
h = 1009660566883490917987475170194560289062628664411983200474597006489640893063715494610197294704009188265361176318190659133132869144519884282668828418392494875096149757008157476595873791868761173517
```

There are many algorithms that make the recovery of discrete logs faster, but under ideal conditions, for numbers as big as the one used, it is still computationally very very expensive to calculate the discrete log $a$. \
Luckily, this isn't one of them.

--- 

## TL;DR
The prime provided generates a group with a smooth order. This lets us split the problem into many smaller and easier subproblems using the Pohlig-Hellman algorithm. These solutions can be combined using CRT to reconstruct the answer. 

---

## Solution
You can use many tools to directly solve this for you, for example, you can use sage as follows - 
```sage
p = 1363402168895933073124331075716158793413739602475544713040662303260999503992311247861095036060712607168809958344896622485452229880797791800555191761456659256252204001928525518751268009081850267001
F = Zmod(p)             # Zmod creates an Integer field mod the number inside
g = F(223)
h = F(1009660566883490917987475170194560289062628664411983200474597006489640893063715494610197294704009188265361176318190659133132869144519884282668828418392494875096149757008157476595873791868761173517)

print(discrete_log(h,g))

# 810642462826781236630409314742801724164468986543937060322593530182136957 
# Converting this to bytes will give you the flag
``` 
So if you wanted a direct solution, this is it.

### Pohlig Hellman Attack

Now I'm gonna talk about the actual attack behind this given value for those of you interested in the math.
I will be assuming familiarity with some basic group theory in the following explanation.

Starting off, we know that $p$ is prime, so the order of its modular ring (and all its generators) will be $p-1$, and the fact that any element of the group, when raised to the order, will be $1\ (mod\ p)$.

### The Vulnerability
What makes finding $a$ difficult is the fact that in large groups, simply going through all powers is not practical, considering how large the order is. However this is something that is very feasible for lower orders.\
So is it possible to convert the problem of finding a larger discrete log to a few smaller discrete logs?\
When the order is smooth (has small factors), YES.

This is exactly the case with our current challenge. Checking for its factors online ([factordb.com](https://factordb.com/index.php?query=1363402168895933073124331075716158793413739602475544713040662303260999503992311247861095036060712607168809958344896622485452229880797791800555191761456659256252204001928525518751268009081850267000)) shows us that its factors are all well under 200. So how do we break this into smaller problems?

Let $x = x_0\cdot x_1 \dots x_n$.\
Now if the order of a generator $g$ is $x$, it means that in its corresponding group, $g^x = 1$. \
Let's define &nbsp; $X_0$ as $\frac{x}{x_0}$ &nbsp; and &nbsp; $g_0$ as $g^{X_0}$ &nbsp; (still in the corresponding mod group).\
This directly implies that the order of $g_0$ is $x_0$, since $$g_0^{x_0} = g^{X_0 \cdot x_0} = g ^ {x} = 1$$
If I want to find a discrete log with the $g_0$ as the base, now I only need to deal with an order of $x_0$ instead of the entire $x$. 

### Creating the Sub-Problems
So how do we apply this to our situation?\
We can factorise the order of the group we have into much smaller factors, each translating to a smaller problem, that gives us some information about the hidden exponent. \
Let $p-1 = p_0^{e_0}\cdot p_1^{e_1} \dots p_n^{e_n}$, $P_i = \frac{p-1}{p_i^{e_i}}$, and $g_i, h_i = g^{P_i}, h^{P_i}$ according to the above convention. If we create smaller problems with respect to each of the prime factors $p_i$ (using $p_i^{e_i}$) as follows - 
$$
\begin{gather*}
g^{a}\equiv h\ (mod\ p) \\
(g^{a})^{P_i}\equiv h^{P_i}\ (mod\ p) \\
(g^{P_i})^{a}\equiv h^{P_i}\ (mod\ p) \\
g_i^{a} \equiv h_i\ (mod\ p) \\
\end{gather*}
$$

We know that each $g_i$ will have a much smaller order, so solving this discrete log problem with the new base will be trivial. But solving this leaves us with a value smaller than its order, which is very unlikely to be the actual answer. Why?

When an element of a group is raised to its order, it wraps back to $1$, so I could be adding the value of the order any number of times to my answer, and it would still hold true. This means that although we couldn't reach the actual value of $a$, we effectively recovered the value of $a\ (mod\ p_i^{e_i})$.

This way, we recover the values of $a$ modulo every coprime factor of $p-1$, leading to a classic use case of the [Chinese Remainder Theorem](https://brilliant.org/wiki/chinese-remainder-theorem/). From here, we simply use CRT to combine them and recover the value of the original $a$.

---

## Code

```python
from Crypto.Util.number import *

def crt(remainders : list, modulos : list) -> int:
    N = 1
    
    # This is the classic method of recovering a modulo p,  given a modulo p1, p2, p3, ... where all factors are pairwise coprime
    for factor in modulos:
        N *= factor
    Nis = []
    for factor in modulos:
        Nis.append(N//factor)
        
    ans = 0
    
    for i in range(len(remainders)):
        ans += remainders[i] * Nis[i] * pow(Nis[i],-1,modulos[i])
        ans %= N
    
    return ans


def pohlig_hellman(p : int, h : int, g : int) -> int:
    # 1. Get order of the group
    order = p-1

    # 2. Store factors
    factors = []
    i = 2
    while order>1:
        pr = i
        exp = 0
        while order%pr == 0:
            order //= pr
            exp +=1
        if exp>0:
            factors.append((pr, exp))
        i += 1
    
    order = p-1
    factors = factors
    print("Factors of the order - ")
    print(factors)
    
    modulos, remainders = [], []
    
    # 3. Solve for each new sub problem by bruteforcing
    for prime, power in factors:
        factor = 1
        
        # This is a limit imposed by me since we are running python. 
        # It might lead to missing the answer sometimes, but it's enough for this problem
        while(factor*prime<10**6 and power>0):
            factor = factor*prime
            power -= 1
        exp = order//factor
        
        # Create new g_i and h_i
        g_i = pow(g,exp,p)
        h_i = pow(h,exp,p)
        
        # Bruteforce for the correct exponent (this might take a while if the factor is large)
        val = 0
        power = 1
        while(power!=h_i):
            power = (power * g_i) % p
            val += 1
            if val==factor:
                print(f"Error in finding discrete log in subgroup with order {factor}")
                exit() 
        
        # Recover information about a
        print(f'a = {val} (mod {factor})')
        modulos.append(factor)
        remainders.append(val)
        
    # 4. Perform CRT to combine answer
    return crt(remainders, modulos)

h = 1009660566883490917987475170194560289062628664411983200474597006489640893063715494610197294704009188265361176318190659133132869144519884282668828418392494875096149757008157476595873791868761173517
p = 1363402168895933073124331075716158793413739602475544713040662303260999503992311247861095036060712607168809958344896622485452229880797791800555191761456659256252204001928525518751268009081850267001
g = 223

print(long_to_bytes(pohlig_hellman(p=p,h=h,g=g)))
```
### Output
```
Factors of the order - 
[(2, 3), (3, 3), (5, 3), (7, 2), (11, 3), (13, 3), (17, 3), (19, 1), (23, 2), (29, 2), (31, 3), (37, 2), (41, 2), (43, 2), (47, 3), (53, 3), (59, 3), (61, 1), (67, 3), (71, 2), (73, 1), (79, 3), (83, 2), (89, 3), (97, 4), (101, 2), (103, 1), (107, 2), (109, 1), (113, 2), (127, 7), (131, 2), (137, 3), (139, 1), (149, 5), (151, 1), (157, 3), (163, 3), (167, 2), (173, 3), (179, 3), (181, 1), (191, 5), (193, 1), (197, 1)]
a = 5 (mod 8)
a = 25 (mod 27)
a = 82 (mod 125)
a = 6 (mod 49)
...
a = 103 (mod 197)
b'utflag{sm00th_cr1m1nal_caught}'
```
---

```
utflag{sm00th_cr1m1nal_caught}
```