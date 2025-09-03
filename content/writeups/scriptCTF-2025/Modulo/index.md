---
title: "Modulo"
date: 2025-09-01T11:43:02+05:30
tags: ['pyjail']
categories: ['misc'] # for | cry | osint | rev | pwn 
authors: ['pastimeplays','_cerealsoup']
description: "damn"
---

# Modulo

<!-- DESCRIPTION -->
> Modulo is so cool!

points: `500`

solves: `18`

handouts: [`jail.py`]

author: `NoobMaster`

---

## Challenge Description

We were given a script that showed us the working of the server.
```python
import ast
print("Welcome to the jail! You're never gonna escape!")
payload = input("Enter payload: ") # No uppercase needed
blacklist = list("abdefghijklmnopqrstuvwxyz1234567890\\;._")
for i in payload:
    assert ord(i) >= 32
    assert ord(i) <= 127
    assert (payload.count('>') + payload.count('<')) <= 1
    assert payload.count('=') <= 1
    assert i not in blacklist

tree = ast.parse(payload)
for node in ast.walk(tree):
    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, ast.Mod): # Modulo because why not?
            raise ValueError("I don't like math :(")
exec(payload,{'__builtins__':{},'c':getattr}) # This is enough right?
print('Bye!')
```
The server took an input from us, and confirmed the following things - 
- All characters had an ASCII value from 32 to 127
- There are at most 1 comparison (< or >) and 1 assignment (=) operator
- None of the characters are blacklisted.
- No binary operations are being used (except modulo?)

Observation - The blacklist contained all lowercase letters except 'c', all numbers and a few symbols

Once these confirmations were made, it ran the payload (our input) with a couple constraints -
1. We do not have access to any builtin functions
2. Any occurences of 'c' (outside a string) will be interpretted as 'getattr' 

--- 

## Solution

### String Formatting

Our first thought was "Since this challenge hints towards modulo a lot, the solution must be heavily dependent on it". So we considered the uses of modulo. You can -
1. Use it as a modulo operator between numbers to get the remainder
2. Use it for string formatting (the forgotten holy grail)

The first use seems pretty pointless for this challenge, since you use numbers to end up with..... numbers.

The second seems very interesting. At first glance it does seem counter productive since even for string formatting, we would need the actual string value stored somewhere, and we can't really achieve anything with only uppercase letters. However, there's a workaround. We can represent characters using numerical(ASCII) values and use those to form strings. Eg. `'%c%c%c'%(65,66,67) = 'ABC'`. 

Another thing that affirmed this approach was how 'c' was the only lowercase letter allowed.

### Forming Numbers

Next comes the problem of forming numbers. The only important thing to note here is that in python, booleans can be interpreted as integer values. `False` is 0, and `True` is 1. Combine this with the fact that we are allowed to use upto one comparison and assignment, it is easy to introduce a number into our jail.

`A='B'<'C'`

This one line assigns `A` the value `True`, which can be used as a 1.

Next comes the problem of making an arbitrary number. If I want to write an 'a', I need the number 97. There's a very neat trick to this. We are barred from using binary operators, but not unary. A simple way to increment a number in python using only unary operators is `~-A`, where `A` is storing a value of 1 (`True`). This gives me a result of 2 because all negative numbers are stored in the [2's complement](https://en.wikipedia.org/wiki/Two%27s_complement) format. That said, if I had to increase a number by 96, I could just do the operations 96 times (a little weird ik but that's how it is)

### The Payload



--- 

```
flag{}
```

