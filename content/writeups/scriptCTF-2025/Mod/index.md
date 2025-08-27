---
title: "Mod"
date: 2025-08-22T14:39:28+05:30
tags: ['Common Sense','Python Fundamentals']
categories: ['crypto'] # for | cry | osint | rev | pwn 
authors: ["pastimeplays"]
description: "Why doesn't this have more solves"
---

# Mod

<!-- DESCRIPTION -->
> Just a simple modulo challenge

points: `285`

solves: `366`

handouts: [`chall.py`]

author: `idk they didn't mention`

---

## Challenge Description

We have a very simple python script that takes an input, returns the modulo of our input with a random 32 byte number, and expects the value of the selected number as our next input

```python
import os
secret = int(os.urandom(32).hex(),16)
print("Welcome to Mod!")
num=int(input("Provide a number: "))
print(num % secret)
guess = int(input("Guess: "))
if guess==secret:
    print(open('flag.txt').read())
else:
    print("Incorrect!")
```

--- 

## Solution

This does not need a writeup go do it on your own.

If you actually didn't get it, what you need to know is that python modulos are always positive, even if my input is negative. So if I enter a $-1$, I will receive $-1 (mod\ n)$ which is basically $n-1$

```
Welcome to Mod!
Provide a number: -1
108100216621666945925699239955352362541854461638982198517531648195503010949768
Guess: 108100216621666945925699239955352362541854461638982198517531648195503010949769
scriptCTF{-1_f0r_7h3_w1n_4a3f7db1_233478219fd1}
```

--- 

```
scriptCTF{-1_f0r_7h3_w1n_4a3f7db1_233478219fd1}
```

