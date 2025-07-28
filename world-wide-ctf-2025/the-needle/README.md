# The Needle

## Challenge Description

> Category: Beginner\
> You are presented with a simple search tool, an interface to a vast and hidden archive of information. Your mission is to find a single, specific secret hidden within. The tool is your only guide, but it is notoriously cryptic. You'll need to use clever queries and careful observation to uncover the prize.

In this challenge, we are given access to a website which has a search tool and nothing else on it. On any generic input, we only get the reply "Nothing here". We are also given a zip file which contains the backend for the web server.

## Reconnaissance

Looking into the files we are given, in the index.php file we can find the logic which is processing our inputs to the website.

```
@$searchQ = $_GET['id'];
@$sql = "SELECT information FROM info WHERE id = '$searchQ'";
@$result = mysqli_query($conn, $sql);
@$row_count = mysqli_num_rows($result);

if ($row_count > 0) {
    echo "Yes, We found it !!";
} else {
    echo "Nothing here";
}
```

Our input is being passed through to an SQL query which is searching the information table. If any rows are returned from the SQL query, then the message "Yes, We found it !!" appears, otherwise we get the "Nothing here" response.

If we then go into the init.sql file, we find that the flag is being inserted as a value into the info table.

```
INSERT INTO info (information) VALUES ('wwf{dummy_flag}');
```

There is no validation that is being done on our input, so this is fully vulnerable to SQL injection. Trying inputs like "'" will result in an error appearing, and using common SQL injection payloads like "a' OR '1'='1" we can get the "Yes, We found it !!" message to appear.

## Solution

Unlike most SQL injection vulnerabilities, we have no access to the result of the SQL query, only whether or not it returned any rows. This means we have to progressively tease out the flag from what we can infer from our SQL queries.

The easiest way to do this is with the RLIKE operator, which matches a string to a regular expression. If we construct a payload such as "a' OR information RLIKE 'wwf\\{.*\\}" to test if a regex matches the flag.

The final step is to create a basic step that can send queries for you, and piece the flag together. I did this using Python, and simply sent GET requests and controlled the payload using the URL. I've included this script under "solve.py".

One thing to mention is that you will have to guess which characters might be in the flag. I simply used all printable characters that were not special characters in mysql regular expressions. Once the script is not able to find more characters you can confirm you solved it with the payload "a' OR information = 'wwf{dummy_flag}"

Flag: `wwf{s1mpl3_bl!nd_sql}`