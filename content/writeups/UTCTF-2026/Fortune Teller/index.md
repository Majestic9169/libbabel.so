---
title: "Fortune Teller"
date: 2026-03-15T21:56:20+05:30
tags: ["beginner"]
categories: ["crypto"] # for | crypto | osint | rev | pwn 
authors: ['pastimeplays']
description: "Learn your math"
---

# Fortune Teller

<!-- DESCRIPTION -->
> Our security team built a "cryptographically secure" random number generator. The lead engineer assured us it was basically AES. He has since been let go.

points: `100`

solves: `547`

handouts: [`lcg.txt`]

author: `@GarvK07`

---

## Challenge Description
This challenge shows us the working of a Linear Congruential Generator (LCG) and exactly why it isn't secure for cryptography.

```
We're using a Linear Congruential Generator (LCG) defined as:

  x_(n+1) = (a * x_n + c) % m

where m = 4294967296 (2^32), and a and c are secret.

We intercepted the first 4 outputs of the generator:

  output_1 = 4176616824
  output_2 = 2681459949
  output_3 = 1541137174
  output_4 = 3272915523

The flag was encrypted by XORing it with output_5 (used as a 4-byte repeating key).

  ciphertext (hex) = 3cff226828ec3f743bb820352aff1b7021b81b623cff31767ad428672ef6
```

--- 

## Solution
What you need to know before solving this is a tiny bit of group theory. Specifically, multiplicative inverses.\
In a modular group (say `mod m`), since all elements are integers, the multipliative inverse of an integer $p$ is not of the usual form $\frac{1}{p}$, but rather, another integer $q$ which satisfies $p*q\equiv1\ (mod\ m)$. To make our lives simpler, this can directly be calculated in python.\
Now that we do know that, we just need to shift our operations to a modular group.\
\
As we can see our goal here is to recover $a$ and $c$, which can just be carried out by simple equation manipulations - 
$$
\begin{gather*}
x_2 \equiv a\cdot x_1 + c\ (mod\ m) \\
x_3 \equiv a\cdot x_2 + c\ (mod\ m) \\
x_3-x_2 \equiv a\cdot (x_2-x_1)\ (mod\ m)\\
a \equiv (x_3-x_2)\cdot(x_2-x_1)^{-1}\ (mod\ m)
\end{gather*}
$$

Now that we have $a$, recovering $c$ is trivial.
$$
\begin{gather*}
c \equiv x2 - a\cdot x_1\ (mod\ m) \\
\end{gather*}
$$
You might have noticed that we needed only 3 outputs to recover $a$ and $c$
```python
# x_(n+1) = (a * x_n + c) % m

m = 4294967296
x1, x2, x3, x4= 4176616824, 2681459949, 1541137174, 3272915523

x32 = x3-x2
x21 = x2-x1

a = (x32 * pow(x21,-1,m))%m
c =  (x2 - a*x1) % m

assert x4 == (a*x3 + c)%m       # Make sure the values are right

key = (a*x4 + c)%m

from Crypto.Util.number import *    # Convenient for conversions and xoring
from pwn import xor

ct = bytes.fromhex('3cff226828ec3f743bb820352aff1b7021b81b623cff31767ad428672ef6')
key_bytes = long_to_bytes(key)
print(xor(ct, key_bytes))  # automatically XOR in a cyclic manner 

# b'utflag{pr3d1ct_th3_futur3_lcg}j\xf2'
```

--- 

```
utflag{pr3d1ct_th3_futur3_lcg}
```

