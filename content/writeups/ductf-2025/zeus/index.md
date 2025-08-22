---
title: "Zeus"
date: 2025-07-22T13:06:52+05:30
tags: ["decompiling"]
categories: ["rev"] # for | cry | osint | rev | pwn 
authors: ["pastimeplays"]
description: "lord of the skies"
---

# Zeus

<!-- DESCRIPTION -->
> To Zeus Maimaktes, Zeus who comes when the norths wind blows, we offer our praise, we make you welcome!

points: `100`

solves: `1053`

handouts: `zeus `

author: `jzt`

## Solution

This was a simple introductory reverse engineering challenge aimed at beginners. We are given an executable file named 'zeus', which when run, sends a  message.

Running it through a [decompiler](https://dogbolt.org) shows us the following code for main -  

```c {linenos=table,hl_lines=[3, 10, 12, 14],linenostart=1,filename="zeus.c"}
int32_t main(int32_t argc, char** argv, char** envp)
{
    void* const var_10 = "To Zeus Maimaktes, Zeus who comes when the north wind blows, we offer our praise, we make you welcome!" ;
    void* const var_18 = "Maimaktes1337";
    int64_t var_58;
    __builtin_memcpy(&var_58, 
        "\x09\x34\x2a\x39\x27\x10\x1f\x0c\x1d\x56\x6c\x5c\x51\x12\x15\x01\x08\x3e\x04\x18\x1c\x1e\x41\x5a\x52\x59\x12\x06\x06\x09\x12\x34\x15\x0b\x17\x6e\x54\x5c\x53\x12\x0e\x0f\x32\x15\x03\x11\x3a\x00\x5a\x4a\x4e", 
        0x33);
    
    if (argc != 3)
        puts("The northern winds are silent...");
    else if (strcmp(argv[1], "-invocation"))
        puts("The northern winds are silent...");
    else if (strcmp(argv[2], var_10))
        puts("The northern winds are silent...");
    else
    {
        puts("Zeus responds to your invocation…");
        int64_t var_98 = var_58;
        int64_t var_90;
        __builtin_memcpy(&var_90, 
            "\x1d\x56\x6c\x5c\x51\x12\x15\x01\x08\x3e\x04\x18\x1c\x1e\x41\x5a\x52\x59\x12\x06\x06\x09\x12\x34\x15\x0b\x17\x6e\x54\x5c\x53\x12", 
            0x20);
        int64_t var_30;
        int64_t var_70_1 = var_30;
        *var_70_1[7] = *var_30[7];
        xor(&var_98, var_18);
        printf("His reply: %s\n", &var_98);
    }
    
    return 0;
}
```

The requirements are very straightforward - 

- We need 2 extra arguments (argc==3)
- The first argument `argv[1]` should be `"-invocation"`
- The second argument `argv[2]` is the contents of `var_10`

Running it with the above arguments directly prints the flag.

```
./zeus "-invocation" "To Zeus Maimaktes, Zeus who comes when the north wind blows, we offer our praise, we make you welcome!"
```

--- 

```
DUCTF{king_of_the_olympian_gods_and_god_of_the_sky}
```

