---
title: "Rolling Pin"
date: 2025-09-02T00:55:16+05:30
tags: ['beginner']
categories: ['rev'] # for | crypto | osint | rev | pwn 
authors: ['pastimeplays']
description: " "
---

# Rolling Pin

<!-- DESCRIPTION -->
> The head baker's gone rogue and locked up the recipe for the perfect pastry swirl inside a secret code. Can you knead your way through layers of fluffy obfuscation and figure out the exact mix of bytes to make it rise just right?

points: `50`

solves: `262`

handouts: [`rolling_pin`]

author: `rvsmvs`

---

## Challenge Description

We get a simple executable that prompts us by saying

'Roll the dough:'

and expects an input.

--- 

## Solution

Send it to the decompilerrrr. Jumping to the useful part of the BinaryNinja decompilation - 
```c
char rotl(unsigned char x, int k) __pure
{
    char var_10 = k;
    return x >> (8 - var_10) | x << var_10;
}

int32_t main()
{
    void* fsbase;
    int64_t rax = *(fsbase + 0x28);
    puts("Roll the dough:");
    char buf[0x48];
    
    if (fgets(&buf, 0x40, __TMC_END__))
    {
        uint64_t var_68_1 = strlen(&buf);
        
        if (var_68_1 && buf[var_68_1 - 1] == 0xa)
            var_68_1 -= 1;
        
        if (var_68_1 == 0x19)
        {
            int64_t var_60_1 = 0;
            
            while (true)
            {
                if (var_60_1 > 0x18)
                {
                    puts("Good job!");
                    break;
                }
                
                if (rotl(buf[var_60_1], var_60_1 & 7) != baked[var_60_1])
                {
                    puts("Not quite done yet");
                    break;
                }
                
                var_60_1 += 1;
            }
        }
        else
            puts("Not quite done yet");
    }
    
    *(fsbase + 0x28);
    
    if (rax == *(fsbase + 0x28))
        return 0;
    
    __stack_chk_fail();
    /* no return */
}
```
The `rotl()` function is clearly left rotating the bits of a byte by an amount that is passed as a parameter.

Jumping into the main function, there's some unneccessary stuff, but we notice that our input is being stored in `buf` and its length is in `var_68_1`. Following that, looks like we need the length of our input to be `0x19` or just `25`.

Then for every character, we need 

`rotl(buf[var_60_1], var_60_1 & 7) == baked[var_60_1]`

Looking around the decompilation, we won't really find the `baked` data anywhere, so we must turn to dissassembly. I used radare2 to find the data.

```
|    :|||   0x0040128f      488d0d7a0d..   lea rcx, obj.baked
```

This line indicated that my values are at the address with the label obj.baked, so I simply printed the first 25 bytes starting from taht address.
```
[0x004010b0]> px 25 @ obj.baked
- offset -  1011 1213 1415 1617 1819 1A1B 1C1D 1E1F  0123456789ABCDEF
0x00402010  62e4 d573 e6ac 9cbd 7260 d1a1 4766 d73a  b..s....r`..Gf.:
0x00402020  6866 7d23 03ae d934 7d                   hf}#...4}
```

From here on out, we just need to reverse the operation performed by the program.
```python
h = "62e4d573e6ac9cbd7260d1a14766d73a68667d2303aed9347d526f6c6c20"
b = bytes.fromhex(h)

def rshift(x,shift):
    return ((x << (8 - shift))&0xff) | (x >> shift)

ans = b''

for i in range(len(b)):
    ans += rshift(b[i],i%8).to_bytes()
    
print(ans)
```

--- 

```
brunner{r0t4t3_th3_d0ugh}
```

