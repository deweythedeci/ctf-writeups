import requests
import string

url = "http://baking-bad-2602c610f88606a4.challs.brunnerne.xyz"
illegal_chars = []

for c in string.printable:
    params = {"ingredient": c}
    print(f"Testing: {c}")
    response = requests.get(url, params=params, timeout=5)
    if "Illegal character detected!" in response.text:
        illegal_chars += c

print(f"Illegal chars: {illegal_chars}")