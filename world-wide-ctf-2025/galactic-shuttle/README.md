# Galactic Shuttle

## Challenge Details

> Category: Beginner \
> I need to catch the next space shuttle but it seems like there are not many seats left! I need two tickets to be able to fly (for me and my buddy). Do you thing you can get me on the shuttle?

In this challenge, we are given access to website (which we have to deploy to visit), and a zip file which contains the code for that webserver. There's also a dockerfile we can use to deploy that server locally for testing purposes.

If we open up the website, we get a simple interface where we can enter a name and either book a seat or claim a boarding pass. However, there is only one boarding pass available and to claim a boarding pass (and get the flag) we need two.

## Reconnaissance

Taking a look at the server's python code we see there is a global enviornment variable named "available_tickets" that is set to 1. Whenever the "/acquire" path receives a GET request, the following code subtracts 1 from the counter and the given user is assigned a ticket. 

```
available_tickets -= 1
ticket_id = uuid.uuid4().hex
purchases.setdefault(user, []).append(ticket_id)
```

If we look earlier in this function, we find a simple check verifies that ensures there are tickets to give out before this operation is done.

```
if available_tickets < 1:
    return jsonify(status="sold_out")
```

Oddly between these steps, there is a call to hashlib which calculates a cryptographic key, although this value goes totally unused.

```
hashlib.pbkdf2_hmac(
    'sha256',
    user.encode('utf-8'),
    b'galactic-shuttle',
    100_000
)
```

Moving onto the /flag path, whenever this path is invoked the following code checks if the given user has more than 1 ticket assigned to them and prints the flag if so.

```
if len(purchases.get(user, [])) > 1:
    return jsonify(flag=FLAG)
```

In both of these functions, users are only differentiated by the name given in the request. However, there aren't any other users in the system we can exploit.

```
user = request.args.get('user')
```

Going to index.html in templates/ we can see that the "Book Your Seat" button is connected to the /acquire function and the "Claim Your Boarding Pass" is connected to the /flag function.

## Exploit

### Race Condition

The critical error here is that a global variable is accessed on a multithreaded web server without any protections. This means a race condition can cause unexpected behavior.

To exploit this, we can use the fact that there is a short window of time between value of available_tickets being checked and it actually being updated. This window is made significantly larger by the hashing algorithm being in the middle.

Essentially, if we can make two acquire requests in a short amount of time with the same name, the server will see available_tickets as 1 for both of them, before either has actually subtracted 1 from them.

To do this, I used Burp Suite's Repeater tool but you could probably also write up a simple Python script. Whatever your method, all you have to do is quickly send two GET requests "/acquire?user=foo". Afterwards, you can reuse that name to claim a boarding pass and receive the flag.

Flag: `wwf{sp4ce_c0nd1t1on_0r_race_c0nd1tI0n?}`