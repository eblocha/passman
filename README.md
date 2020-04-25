Passman
=======
Password manager command line interface written in python.

**Do not use this implementation for sensitive passwords. This is only an exercise, and is not as secure as something like KeePass**  
**Passwords and keys cannot be easily erased from memory in Python**

Usage
-----
Create a file called `vault_config.json` in the same directory as vault.py:  
`{"root": "path/to/vault/folder"}`

Start the shell
```
>python shell.py
Welcome to Vault!
Enter "-h" or "--help" for help
VAULT > 
```

Create a new vault
```
VAULT > --new main
Master password (enter to abort): 
Re-enter master password: 
(main) >>> 
```

Create an entry in the vault
```
(main) >>> --add google.com
Enter a username: user
Enter a password: 
(main) >>> 
```

Get an entry in the vault
```
(main) >>> --get google.com
google.com
{'username': 'user', 'password': 'password'}
(main) >>> 
```
You can list multiple entries after `--get` to get more than one at a time

List of commands available inside the vault:
```
--add: add or update entry to database
--rem: remove entry from database
--get: get an entry's value from database
--list: list all entry keys
--exit: exit and save the database
```

When you exit the vault, all contents will be re-encrypted, then saved.