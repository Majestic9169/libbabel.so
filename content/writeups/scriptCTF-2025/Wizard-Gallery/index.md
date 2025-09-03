---
title: "Wizard-Gallery"
date: 2025-08-21T10:25:35+05:30
tags: ["ImageMagick", "CVE-2022-44268"]
categories: ["web"] # for | cry | osint | rev | pwn 
authors: ["_cerealsoup"]
description: "Everything is osint if you look hard enough."
---

# Wizard-Gallery

> The council's top priority is to protect the flag, no matter the cost.
Oh hey look, it's a photo gallery. What could go wrong? Hint: RCE is a luxury nowadays.

Author: `Ashray Shah`

---

## Challenge Description

They've given an image-upload service. The logo file is served separately at `/logo`.
There's also a `/logo-sm` endpoint that uses `ImageMagick` to convert `logo.png`
to a smaller size (`logo-sm.png`) and serve that file.

## Solution

### Attempting File Validation Bypass (Red-Herring)

So obviously, the first thing I tried was to upload non-image files.

```py
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
BLOCKED_EXTENSIONS = {'exe', 'jar', 'py', 'pyc', 'php', 'js', 'sh', 'bat', 'cmd',
                      'com', 'scr', 'vbs', 'pl', 'rb', 'go', 'rs', 'c', 'cpp', 'h'}

# --- snip ---

def allowed_file(filename):
    if '.' not in filename:
        return False
    basename = os.path.basename(filename)
    if '.' not in basename:
        return False
    extension = basename.rsplit('.', 1)[1].lower()
    if extension in BLOCKED_EXTENSIONS:
        return False
    return extension in ALLOWED_EXTENSIONS

def is_blocked_extension(filename):
    if '.' not in filename:
        return False
    basename = os.path.basename(filename)
    if '.' not in basename:
        return False
    extension = basename.rsplit('.', 1)[1].lower()
    return extension in BLOCKED_EXTENSIONS

```

Hmm... Seems like they've just validated filenames by extension string.
They don't check for actual MIME-type, but whatever.

### Directory Traversal

Looking into the handler for `/upload` endpoint...

```py
    original_filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    file.save(file_path)
```

Yeah, that's plain directory traversal right there.
I can manipulate the uploaded image name to something like `../../path/to/wherever`.
Cool, that means I can overwrite the `logo.png` file at project root with anything.

### CVE-2022-44268: Arbitrary File Read in ImageMagick

The ImageMagick version used in the app is vulnerable to Arbitrary File Read attack
([CVE-2022-44268](https://www.cve.org/CVERecord?id=CVE-2022-44268))

> When ImageMagick performs operations such as resizing on a PNG file, it may
include the content of a system file, given that the magick binary has the
necessary permissions to read it. This vulnerability arises due to the mishandling
of textual chunks within PNG files.
> A malicious actor can exploit this vulnerability by crafting a PNG file or using
an existing one and adding a textual chunk type (tEXt). These chunks consist of a
keyword and a text string. In this case, if the keyword matches the string "profile"
(without quotes), ImageMagick will interpret the accompanying text string as a filename
and attempt to load its content as a raw profile. As a result, when the resized image
is downloaded, it will contain the content of the remote file specified by the attacker.

For more information, see this [article from MetabaseQ](https://www.metabaseq.com/imagemagick-zero-days/).

Okay so, the `convert` command is vulnerable. Is it being used?

```py
@app.route('/logo-sm.png')
def logo_small():
    # A smaller images looks better on mobile so I just resize it and serve that
    logo_sm_path = os.path.join(app.config['UPLOAD_FOLDER'], 'logo-sm.png')
    if not os.path.exists(logo_sm_path):
        os.system("magick/bin/convert logo.png -resize 10% " 
      + os.path.join(app.config['UPLOAD_FOLDER'], 'logo-sm.png'))
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'logo-sm.png')
```

Perfect. We can use this to leak the `flag.txt` file.
A little digging around on github got me this
[POC](https://github.com/entr0pie/CVE-2022-44268) of the exploit.

### Crafting the PNG

After cloning the POC script, I simply ran:

```sh
python3 CVE-2022-44268.py flag.txt
```

This creates the `output.png` file, which I'm going to replace the `logo.png` with.

### Finishing the Exploit

Finally, I uploaded the `output.png` to the server instance, using Burpsuite to rename
it to `../logo.png`.

Now I just had to hit the `/logo-sm` endpoint. It created the minified version of
the overwritten logo file.

`cat`-ing the `logo-sm.png` reveals this piece of _suspiciously hex-shaped_ string:

```
7363726970744354467b7430305f6d7563685f6d343669635f3139386535616162306238637d0a
```

Noice, just unhex it now.

---

```
scriptCTF{t00_much_m46ic_198e5aab0b8c}
```
