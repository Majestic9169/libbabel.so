---
title: "Textopolis"
date: 2025-09-02T00:33:23+05:30
tags: ['beginner']
categories: ['rev'] # for | crypto | osint | rev | pwn 
authors: ['pastimeplays']
description: "nice intro to rev"
---

# Textopolis

<!-- DESCRIPTION -->
> I just heard of this brand new city! 🏙️
Textopolis? 🤔
It sounds quite cool 😎
I want to move there! ✈️

>It might be useful to send a spy before attempting to enter the city!

>This challenge may not work fully with WSL, if you choose to run it, please use Powershell.

points: `40`

solves: `125`

handouts: [`textopolis.exe`]

author: `Quack`

---

## Challenge Description

We are provided with an executable file which asks us for our favorite emoji. Also, the 'spy' in the description is linked to the GitHub repo for a tool called ILSpy, which is a .NET decompiler.

--- 

## Solution

Since this is a rev challenge, we send our executable straight into the decompiler. Here, we have been purposefuly pointed towards ILSpy, so obviously, that's what we'll be using.

Digging into the main function in out decompiled output, we see this - 
```java
Console.OutputEncoding = Encoding.UTF8;
Console.InputEncoding = Encoding.UTF8;
Console.WriteLine("Welcome to Textopolis! \ud83e\udd20");
Console.WriteLine("Home of all your favorite emojis! \ud83d\ude03");
Console.WriteLine("Do you have what it takes to be an emoji? Let's find out! \ud83d\ude80" + Environment.NewLine);
Console.WriteLine("Please enter your favorite emoji:");
string text = Console.ReadLine() ?? string.Empty;
if (favouriteEmoji(text))
{
    Console.WriteLine(Environment.NewLine + "Good choice! That is my favorite emoji too!");
}
else
{
    Console.WriteLine(Environment.NewLine + "Don't worry, keep trying! Every emoji has its day! \ud83c\udf1f");
    Environment.Exit(0);
}
```
and from this, looking into the `favoriteEmoji` function that was used here leads us to -
```java
private static bool favouriteEmoji(string emoji)
{
	if (emoji == "‼")
	{
		return true;
	}
	return false;
}
```
This gives us the expected emoji to enter. But wait, there's more! This check in main is followed by - 
```java
Console.WriteLine("But wait! We need check your emoji passport before you can enter! \ud83d\udec2");
Console.WriteLine("Please enter your emoji passport:");
string passport = Console.ReadLine() ?? string.Empty;
if (emojiPassportCheck(passport))
{
    Console.WriteLine(Environment.NewLine + "Congratulations! You are now eligible for residence in Textopolis! \ud83c\udf89");
}
else
{
    Console.WriteLine(Environment.NewLine + "Oh no! Your emoji passport is not valid. Please get it renewed. \ud83d\ude22");
    Environment.Exit(0);
}
```

So once again, we head to the `emojiPassportCheck` and its corresponding requirements - 
```java
private static bool emojiPassportCheck(string passport)
{
	Array.Reverse(emojiPassport);
	return passport == string.Join("", emojiPassport);
}
```
```java
private static string[] emojiPassport = new string[9] { "☺", "♦", "♣", "♥", "♠", "♪", "☼", "♫", "☺" };
```

Last step - 
```java
Console.WriteLine("Before you can become a full resident of Textopolis, you must choose your new name! \ud83d\udcdd");
Console.WriteLine("Please enter your new emoji name:");
string text2 = Console.ReadLine() ?? string.Empty;
if (validEmojiName(text2))
{
    Console.WriteLine(Environment.NewLine + "Welcome to Textopolis, " + text2 + "! You are now a proud emoji resident! \ud83c\udf8a");
}
else
{
    Console.WriteLine(Environment.NewLine + "Your emoji name is not valid. Please try again with a different name. \ud83d\ude1e");
    Environment.Exit(0);
}
Console.WriteLine("As a thank you for becoming a resident, here is a special emoji gift for you: \ud83c\udf81");
Console.WriteLine("brunner{\ud83e\udd11\ud83e\udd17\ud83d\ude07\ud83d\ude1b" + string.Join("", emojiPassport) + "\ud83e\udd14\ud83d\ude0f" + text + "\ud83d\ude0e\ud83e\udd2f\ud83e\udd20\ud83e\udd73\ud83d\ude35\ud83e\udd71\ud83e\udd10\ud83e\udd75\ud83e\udd76\ud83d\udc7b}");
Console.WriteLine("Enjoy your stay in Textopolis! \ud83c\udfd9\ufe0f");
```
```java
private static bool validEmojiName(string name)
{
	if (name.Length >= 4 && name.Length <= 10 && name.Contains("⌂") && !name.Contains("♣") && name.Contains("¿") && !name.Contains("♦") && !name.Contains("☻") && name.Contains("■") && !name.Contains("♥"))
	{
		return true;
	}
	return false;
}
```


Now technically, you could've directly extracted the flag from the line - 

`Console.WriteLine("brunner{\ud83e\udd11\ud83e\udd17\ud83d\ude07\ud83d\ude1b" + string.Join("", emojiPassport) + "\ud83e\udd14\ud83d\ude0f" + text + "\ud83d\ude0e\ud83e\udd2f\ud83e\udd20\ud83e\udd73\ud83d\ude35\ud83e\udd71\ud83e\udd10\ud83e\udd75\ud83e\udd76\ud83d\udc7b}");`

but I feel like it's more fun this way :P

--- 

```
brunner{🤑🤗😇😛☺♫☼♪♠♥♣♦☺🤔😏‼😎🤯🤠🥳😵🥱🤐🥵🥶👻}
```

