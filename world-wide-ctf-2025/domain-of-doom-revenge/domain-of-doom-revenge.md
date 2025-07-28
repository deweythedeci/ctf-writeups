# Domain of Doom Revenge

## Challenge Details

> Category: Web\
> You're querying domains, but some lead to dangerous places\
> The flag is hidden in an environment variable.

In this challenge, we are given a web server we can spawn and a code.zip which contains a Dockerfile and the source code to run that server.

There is a slight error in the code.zip which you may have to modify to get it functional. This code block is missing from the app.py file which will make the web server give an error 500 whenever you try to run it.

```
@app.route('/about')
def about():
    return render_template('about.html')
```

If you are unfamiliar with docker, you can navigate the folder where you extracted the code.zip and run the following command to quickly get started.

```
docker run $(docker build -q .)
```

## Reconnaissance

### Inspecting app.py

Once we've opened up the code we can see its a very basic Flask server. There's a home, about, and contact page, but only the contact page has anything of interest to us. If we look at the code in app.py under the contact function we find this interesting code block.

```
command = f'dig +short -t A {safe_domain}'
resolve_result = subprocess.Popen(
    command, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.STDOUT, 
    shell=True
).communicate()[0].strip().decode() or 'Could not resolve the provided domain/ticket!'
```

We can see that the subprocess python library is being used to execute a dig command with the target hostname being a variable safe_domain. We can also see that the shell parameter is being set to True. This means whatever string is passed into this function is going to be interpreted for the shell.

If we look back into the code to see where safe_domain is being defined we can see it is user controlled! Or at least, partially. It gets filtered by another function safe_domain_check.

```
subject_domain = request.form.get('subject', '').lower()
...
safe_domain = safe_domain_check(subject_domain)
```

If we look at safe_domain_check, we can see it will only be let through if the input matches a particular regex. This regular expression appears to be meant to only let through relatively "normal" web addresses, like www.google.com or abc.foobar.net.

```
def safe_domain_check(domain):
    is_safe = re.search(r'^([a-z]+.)?[a-z\d\- ]+(\.(com|org|net|sa)){1,2}', domain)
    return is_safe.group(0) if is_safe else None
```

If we look at where the output of the dig command goes, we see that the stdout is captured and then rendered onto the webpage using flask's library as well as the domain we provided. 

If we then go to the web server under contact we see a form that matches what we expect. There is a form we can fill out, and whatever URL we put under "Subject / Ticket Number" will get passed to the dig command. For example, if we send "www.google.com" the website will display something like "142.250.69.164".

### Issues with the Regex

If we look at that regex closely we can spot a few critical errors.

The "[a-z\d\- ]+" part of the regex allows dashes and spaces which lets us add extra flags. For example, you can submit the subject "-h .com" to get the list of all flags dig accepts. This is neat, but none of the flags in dig are helpful for exfiltrating the flag enviornment variable.

However, the "^([a-z]+.)?" part of the regex has a dot in it but it is mistakenly not escaped with a backslash. This means we can send something like "a; pwd .com" and run any command we want.

## Exploit

Our first instinct would be to send something like "a; printenv .com" but this doesn't work. If given an argument printenv will only display the enviornment variable with the name ".com". You also can't specify the flag variable because the name is in uppercase and the regex only allows lowercase.

The trick is to dig through all the functions on the server that print all of the enviornment variables and has a flag that will accept ".com", ".org", ".net", or ".sa" as an input without issue. The command I found was env with the -u (unset) flag.

The payload I used was: `a; env -u .com`.

All you have to do is start up the server, input this as your subject and read the flag from the output on the webserver.

The flag: `wwf{cmd_injectlon_rEv3ngE_!!!}`