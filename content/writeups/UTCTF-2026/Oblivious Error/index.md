---
title: "Oblivious Error"
date: 2026-03-17T20:06:17+05:30
tags: ['beginner', '1-2 Oblivious Protocol']
categories: ['crypto'] # for | crypto | osint | rev | pwn 
authors: ['pastimeplays']
description: "1-2"
---

# Oblivious Error

<!-- DESCRIPTION -->
> My friend made an RSA-based 1-2 oblivious transfer protocol program. I don't know what that means but I need to know quick because I accidentally deleted his code! I replaced the part I deleted with the following code in the text file below, but now one of the messages is undecodable and I don't know why!
>
> Can you decode the lost message?

points: `100`

solves: `360`

handouts: [`my-code.txt`]

author: `@jayscx`

---

## Challenge Description

We will be using the 1-2 oblivious transfer protocol on this one.\
This is what the handout says - 
```
while True:
    try:
        print("Please pick a value k.")
        k = int(input())
        break
    except ValueError:
        print("Invalid value. Please pick an integer.")
        print("Please pick a value k.")
        k = int(input())

v = (x0 + (int(k) ^ e)) % N

``` 

--- 

## Solution

### The 1-2 Oblivious Transfer Protocol
This protocol has two simple goals -
- to let the reciever pick one of two messages without letting the sender know which one
- to let the sender transmit the selected message without letting the reciever understand the other one

At first glance, it might seem confusing as to how the sender can hide the right message without knowing which one it is, so let's go through the flow of the protocol step by step.

1. To start with, the sender Alice has two messages that she is ready to transfer, $m_0$ and $m_1$.
Alice begins by sharing her RSA public key $(N,e)$ with Bob while keeping her private key $d$ hidden.

$$ Alice \ \ \xrightarrow{N,e} \ \ Bob $$ 

2. Alice now sends two random values $x_0$ and $x_1$ to Bob (we'll see why).

$$ Alice \ \ \xrightarrow{x_0,x_1} \ \ Bob $$ 

3. Bob decides that he wants message $m_b$ and generates a random value $k$ lesser than $N$.\
Now depending on his value of $b$ (0 or 1), he generates a $v$, as shown below, and returns it. 

$$ Alice \ \ \xleftarrow{v = (x_b + k^{e})\ mod\ N} \ \ Bob $$ 

4. Because of the two random values, $x_0$ and $x_1$, Alice does not know which message was picked, or even the value of $k$. So she calculates two candidate $k$s -\
$k_0 = (v-x_0)^{d}\ mod\ N$\
$k_1 = (v-x_1)^{d}\ mod\ N$\
\
One of these is equal to the $k$ that Bob picked, but since it was randomly chosen, Alice doesn't know which one it is.\
Note that Bob won't be able to recover the other $k$ either, since he lacks the value of $d$ needed to calculate it.

5. Alice finally just sends each $k$ added to its corresponding message.\
$m_0' = (m_0 + k_0)\ mod\ N$\
$m_1' = (m_1 + k_1)\ mod\ N$

$$ Alice \ \ \xrightarrow{m_0', m_1'} \ \ Bob $$ 

6. Bob, knowing which $m$ he picked, recovers it by subtracting his $k$.\
$m_b = (m_b' - k)\ mod\ N$

This transfer fulfills both the goals.

### The Vulnerability
```python 
v = (x0 + (int(k) ^ e)) % N
``` 
This line is the reason why the situation is easy to break. One of the first issues you can spot here is the fact that the `^` operator has been used for exponentiation, but this is the XOR operator in Python.\
Second, you might have noticed that if the overall $k_i$ turns out to be zero, the sender sends the intended message unencrypted.

### Manipulating With Our k
Starting off, what if I made my $v = x_0$? \
It would calculate my $k_0$ to be $0$! This means that $m_0$ will be returned as is by the server. \
Let's try this by setting $k = e$ (since we are XORing instead of exponentiating)
```
┌──(pastimeplays㉿MSI)-[~]
└─$ nc challenge.utctf.live 8379
Here's your entrance key!
N = 5990367315336184534697326483452971614741541936021432036791845172047265179678439102741711782724711960177422760001745132596172663607659623081093596011589397
e = 65537
Here are my random x values!
x0: 5483361751746128116942583190712855682356591243085737553970320598490725027405518008821935481414471786238047509413046158111160986853415487966370093410863327
x1: 3749182735849506575109007991369084329926705303608295813277259878148094369399352334900622662871912065952192037191982265092027946182414158627072102808305793
Please pick a value k.
65537
Here are your messages!
Message 1:  3222194627663678435710450691734050598987331102631121234186273477219287501171174516697552184334280794126685068606242824303996273307765957990931162090767994
Message 2:  14614909182015656433423375395560694783276217129595018028195683192534693780147751705041670356317823574397
```
One of these messages looks interesting. Converting it to text leads us to `hgsynt{Pbatengf! Lbh pnhtug n erq ureevat!}`.\
Applying ROT13 (Caeser Cipher) on this makes it `utflag{Congrats! You caught a red herring!}`.

Close, but it looks like this was not the intended flag. So we do the only other thing we can, and try to target $m_1$ instead of $m_0$. We have a similar approach, but our target this time is to make $v = x_1$.\
Since we have both $x_0$ and $x_1$ values, we can manipulate $v$ by setting our $k$ to $(x_1-x_0)\oplus e$, since
$$
\begin{gather*}
v\ =\ x_0 + (k\oplus e)\ =\ x_0 + ((x_1 - x_0)\oplus e \oplus e) \\
\ =\ x_0 + (x_1 - x_0)\ =\ x_1
\end{gather*}
$$

Let's see what this gives us
```
┌──(pastimeplays㉿MSI)-[~]
└─$ nc challenge.utctf.live 8379
Here's your entrance key!
N = 6844777368733302313445376450966053442723544406291939962641283994195492196834031698504270646438774422507829612165033876906761748329150664480176588785817049
e = 65537
Here are my random x values!
x0: 1802213900399621415431782255877137293240350247755112853525544480136320705545867086084070903407087902672088495541946051074309470796135612585827079666208438
x1: 5395223406189616993612568839907381466205299178349402136851513264607273542429119095362676134378492670033429685897598330655853635219765379047054622333007248
Please pick a value k.
3593009505789995578180786584030244172964948930594289283325968784470952836883252009278605230971404767361341190355652279581544164423629766461227542666733275
Here are your messages!
Message 1:  4124066285856350120154821419138403777810656734140525405779509134907038323557389920421693312597003143845845898180080381555684325696857307328274937917975891
Message 2:  16441782473165749985269251414928450202051900518929647105868978172963309169080628914206924705003483790602
```

--- 

```
utflag{my_obl1v10u5_fr13nd_ru1n3d_my_c0de}
```

