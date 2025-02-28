# CTF 101
This is the introductory challenge. When you download the zip file it contains a basic Flask application. Looking at the code in the `app.py` file we find the following two lines:
```
output = subprocess.check_output(f"echo {name}", shell=True, text=True, stderr=subprocess.STDOUT)
flash(f"Hello, {output.strip()}! Good luck!", "success")
```

The first line executes the input from the form directly in echo, then the output of that is sent to the return form.

## Solution
If we enter `$(cat flag.txt)` into the form, the code will execute our sub-command and send the output of the flag file to the browser for us.

Flag: flag{3b74fc0628299870edabc5072b25cf78}

---

# Screaming Crying Throwing Up
In this challenge we are provided one file: `screaming.bin`. When inspecting this file with exiftools we see the following:
```
File Name                       : screaming.bin
Directory                       : .
File Size                       : 82 bytes
File Modification Date/Time     : 2025:02:27 12:22:58-07:00
File Access Date/Time           : 2025:02:27 12:29:23-07:00
File Inode Change Date/Time     : 2025:02:27 12:22:58-07:00
File Permissions                : -rwxrwxrwx
File Type                       : TXT
File Type Extension             : txt
MIME Type                       : text/plain
MIME Encoding                   : utf-8
Byte Order Mark                 : No
Newlines                        : (none)
Line Count                      : 1
Word Count                      : 1
```

Seeing that the MIME Encoding is UTF-8 leads me to think this may be a plain text file with a .bin extension.
Running cat on the file produces this:
`a̮ăaa̋{áa̲aȧa̮ȧaa̮áa̲a̧ȧȧa̮ȧaa̲a̧aa̮ȧa̲aáa̮a̲aa̲a̮aaa̧}`

There is a hint the puzzle that this is associated with the XKCD web comic, and a quick search finds us the [Screaming Crying cypher](https://xkcd.com/3054/) It sure looks like this is what we have here. Another search found me [this encoder/decoder](https://scream-cipher.netlify.app/). Putting our cypher text into that gives us the answer.

Flag: flag{edabfbafedcbbfbadcafbdaefdadfaac}

---

# Technical Support
This is another introductory 'challenge'. All we have to do for this one is join the Snyk Discord server. In there we find a channel called `open-help-ticket`, in that channel we find a pined message that instructs us not to create a ticket, but provides us the flag.

Flag: flag{d7aa66ea0edd20221820c84ecc47aee9}

---

# Read the Rules

This is another basic introductory challenge, you are directed to a web page that has the rules of the CTF listed and given the hint: If you look closely you can even find a flag hidden on this page. If we view the source code for that page we find the flag in a comment near the bottom of the page.

Flag: flag{90bc54705794a62015369fd8e86e557b}

---

# Zero Ex Six One

For this challenge we are provided and encrypted file called `flag.txt.encry`. The file content when output with cat is: `0x070x0d0x000x060x1a0x020x540x510x050x590x530x020x510x000x530x540x070x520x040x570x550x550x050x510x560x510x530x030x550x500x050x030x050x510x590x540x000x1c`

This looks like a long string of hexadecimal characters, but most of them aren't in the standard ascii range. Some of the hints we are given:
- I'm XORta of ideas for how to get this flag.
- The name of the challenge is a bit of a hint 0x61 is the letter `a` in ascii. 

For this one I used [Cyber Chef](https://cyberchef.org/#recipe=From_Hex('0x')XOR(%7B'option':'UTF8','string':'a'%7D,'Standard',false)&input=MHgwNzB4MGQweDAwMHgwNjB4MWEweDAyMHg1NDB4NTEweDA1MHg1OTB4NTMweDAyMHg1MTB4MDAweDUzMHg1NDB4MDcweDUyMHgwNDB4NTcweDU1MHg1NTB4MDUweDUxMHg1NjB4NTEweDUzMHgwMzB4NTUweDUwMHgwNTB4MDMweDA1MHg1MTB4NTkweDU0MHgwMDB4MWM)
1. We convert the string into ascii on the delimiter of 0x
2. We XOR each character with the letter `a` from the hint in the challenge name
3. Profit!

This gives us the flag for this challenge.

Flag: flag{c50d82c0a25f3e644d0702b41dbd085a}

---

## WHO IS JH

This challenge required you to discover the vulnerabilities in a website that lets users upload evidence to support the mutli-john-hammond conspiracy. This challenge had a few layers to it.
- The flag file is in the root of the file system at `/flag.txt`
- The code for the upload page does a very basic whitelist check on the file extension to only allow .jpg, .gif. and .png file types to be uploaded.
- The upload code prepends a randomly generated unique id to the filename you supply then saves the file into the uploads directory.
- The conspiracy page accepts a language parameter that can include folder structures and it will then render the php file you specify with that parameter.

The attack angle I came up with was to:
1. Create a malicious file that has the following PHP code in it, and name the file `get_flag.php.jpg`
``` PHP
<?php echo readfile('/flag.txt') ?>
```
1. Use the language parameter on the conspiracy page to identify what the file name that was uploaded was called on the server after the unique id was added to the front.
	- `conspiracy.php?language=logs/site_log.txt`
2. Use the language parameter again to render our malicious file from the `/uploads` directory.
	- `conspiracy.php?language=uploads/67c0f14e55c16_get_flag.php.jpg`
3. Profit!

Flag: flag{6558608db040d1c64358ad536a8e06c6}

---

## Free Range Packets

This challenge provides you with a packet capture from a bluetooth device that has the flag data in it.
I used Wireshark to filter down the packets to just the ones with the flag data using this filter `bluetooth and _ws.col.protocol == "L2CAP" and _ws.col.def_dst == "remote ()"` then I identified that the character in the payload byte array [9-13] contained the characters of the flag.

Next I exported only the payloads from the selected packets into a text file and using a text editor I was easily able to remove the extra data from each line and combine them together to get the flag.

Flag: flag{b5be72ab7e0254c056ffb57a0db124ce}

---

## A Powerful Shell

For this challenge we are given a powershell script. When the script is executed it tells us that we are missing the key.
``` bash
Nice
try!
But
you
need
the
magic
key!
```

Looking at the code we find a big long string that looks to be base64 encoded, and the lines that follow confirm that.

``` Powershell
# Embedded and encoded layer 2

$encoded = "JGRlY29kZWQgPSBbU3lzdGVtLkNvbnZlcnRdOjpGcm9tQmFzZTY0U3RyaW5nKCdabXhoWjNzME5XUXlNMk14WmpZM09EbGlZV1JqTVRJek5EVTJOemc1TURFeU16UTFObjA9JykNCiRmbGFnID0gW1N5c3RlbS5UZXh0LkVuY29kaW5nXTo6VVRGOC5HZXRTdHJpbmcoJGRlY29kZWQpDQoNCiMgT25seSBzaG93IGZsYWcgaWYgc3BlY2lmaWMgZW52aXJvbm1lbnQgdmFyaWFibGUgaXMgc2V0DQppZiAoJGVudjpNQUdJQ19LRVkgLWVxICdTdXAzclMzY3IzdCEnKSB7DQogICAgV3JpdGUtT3V0cHV0ICRmbGFnDQp9IGVsc2Ugew0KICAgIFdyaXRlLU91dHB1dCAiTmljZSB0cnkhIEJ1dCB5b3UgbmVlZCB0aGUgbWFnaWMga2V5ISINCn0="

$bytes = [Convert]::FromBase64String($encoded)

$decodedScript = [System.Text.Encoding]::UTF8.GetString($bytes)
```

Taking that $encoded string over to Cyber Chef again and base64 decoding it give us this bit of powershell code.

``` Powershell
$decoded = [System.Convert]::FromBase64String('ZmxhZ3s0NWQyM2MxZjY3ODliYWRjMTIzNDU2Nzg5MDEyMzQ1Nn0=')
$flag = [System.Text.Encoding]::UTF8.GetString($decoded)

# Only show flag if specific environment variable is set
if ($env:MAGIC_KEY -eq 'Sup3rS3cr3t!') {
    Write-Output $flag
} else {
    Write-Output "Nice try! But you need the magic key!"
}
```

In here we find yet another string that looks to be base64 encoded. Coupled with the comment from the first file that mentioned Layer 2. We base64 decode this one and get the flag!

Flag: flag{45d23c1f6789badc1234567890123456}