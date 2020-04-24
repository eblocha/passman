import vault
import getpass

def add(db,args):
    if not args:
        args = input('Website(s): ').split(' ')

    entry = dict()
    for site in args:
        entry[site] = dict()
        entry[site]['username'] = input('Enter a username: ')
        entry[site]['password'] = getpass.getpass('Enter a password: ')
            
    db.update(entry)
    return db

def remove(db,args):
    if not args:
        args = input('Website(s): ').split(' ')

    print('Entries found: ')
    for key in args:
        if key not in db:
            print(f'{key} not found in vault.')
        else:
            print(key)
    delete = input('Delete the above entries? [y/n]: ').lower()
    if delete=='y':
        for key in args:
            if key in db:
                del db[key]
    return db

def retrieve(db,args):
    if not args:
        args = input('Website(s): ').split(' ')
    
    for site in args:
        if site in db:
            print(f'{site}:')
            print(db[site])
        else:
            print(f'{site} not found in vault.')

def list_keys(db):
    keys = list(db.keys())
    if keys:
        for key in keys:
            print(key)
    else:
        print('No entries.')
        