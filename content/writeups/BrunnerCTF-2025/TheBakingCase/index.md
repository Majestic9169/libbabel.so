---
title: "TheBakingCase"
date: 2025-09-01T22:23:38+05:30
tags: ['beginner']
categories: ['misc'] # for | crypto | osint | rev | pwn 
authors: ['pastimeplays']
description: "Love these easy ones"
---

# TheBakingCase

<!-- DESCRIPTION -->
> I hid a message for you here, see if you can find it! Take it slow, little by little, bit by bit.

points: `40`

solves: `478`

handouts: 

author: `H4N5`

---

## Challenge Description

We are given a text message - 
```
i UseD to coDE liKe A sLEEp-dEprIVed SqUirRel smasHInG keYs HOPinG BugS would dISApPear THrOugh fEAr tHeN i sPilled cOFfeE On mY LaPTop sCReameD iNTerNALly And bakeD BanaNa bREAd oUt oF PAnIc TuRNs OUT doUGh IS EasIEr tO dEbUG ThaN jaVASCrIPt Now I whIsPeR SWEEt NOtHIngs TO sOurDoUGh StARtERs aNd ThReATEN CrOissaNts IF they DoN'T rIsE My OVeN haS fEWeR CRasHEs tHAN mY oLD DEV sErvER aNd WHeN THInGS BurN i jUSt cAlL iT cARAMElIzEd FeatUReS no moRE meetInGS ThAt coUlD HAVE bEeN emailS JUst MufFInS THAt COulD HAvE BEen CupCAkes i OnCE tRIeD tO GiT PuSh MY cInnAmON rOLLs aND paNICkED WHEn I coUldn't reVErt ThEm NOw i liVe IN PeaCE uNLESs tHe yEast getS IDeas abOVe iTs StATion oR a COOkiE TrIES To sEgfAult my toOTH FILlings
```
and several hints towards 'casing'.

--- 

## Solution

Paying attention to the author's emphasis on cases, there are multiple things that you can try out, such as considering only uppercase letters, or lowercase letters, and so on.

What you arrive to in the end, is treating them as binary digits. The solution simply requires you to treat an uppercase letter as a `1` and a lowercase letter as a `0`. This leads you to a binary - 

```010010000110010101110010011001010010000001101001011100110010000001110100011010000110010100100000011001100110110001100001011001110010000001100010011100100111010101101110011011100110010101110010011110110100100101011111011011000110100101101011011001010101111101000010011000010110101101101001011011100110011101011111010011010110111101110010011001010101111101010100011010000110000101110100010111110101000001110010011011110110011101110010011000010110110101101101011010010110111001100111011111010010000001100101011000010111001101111001001000000111000001100101011000010111001101111001001000000011111100000```

which in turn, translates to -

`Here is the flag brunner{I_like_Baking_More_That_Programming} easy peasy ?`

--- 

```
brunner{I_like_Baking_More_That_Programming}
```

