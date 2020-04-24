"""Provide a shell to interact with databases"""
import vault
import getpass
import os
import main_commands as mc
import db_commands as dbc

def getargs(command):
    """Split off arguments from command"""
    args = command.split(' ')
    command = args[0].lower()
    args = args[1:]
    return command, args

def _help(commands):
    print('\nCommands:\n')
    for key in commands:
        print(f'{key}: {commands[key]}')
    print('\n')

def main():
    """Main shell routine to work with multiple databases"""
    commands = {
        '--new [vault name]': 'create new vault',
        '--open [vault name]': 'open existing vault',
        '--exit': 'exit shell'
    }
    while True:
        command = input(f'VAULT > ')
        command, args = getargs(command)
        if command in ['-h','--help']:
            _help(commands)
        elif command in ['-n','--new']:
            mc.main_new(args)
        elif command in ['-o','--open']:
            mc.main_open(args)
        elif command in ['-e','--exit']:
            return
        elif command:
            print('Command not recognized. Enter "-h" or "--help" for help')


def db_shell(name,master_pwd):
    """Initialize a new shell inside the given DB with the given master password"""
    db, master_key = vault.open_db(name,master_pwd)
    commands = {
        '--add': 'add or update entry to database',
        '--rem': 'remove entry from database',
        '--get': 'get an entry\'s value from database',
        '--list': 'list all entry keys',
        '--exit': 'exit and save the database'
    }
    while True:
        command = input(f'({name}) >>> ')
        command, args = getargs(command)
        if command in ['-h','--help']:
            _help(commands)
        elif command in ['-e','--exit']:
            vault.write_file(name, db, master_pwd, master_key)
            return
        elif command in ['-a', '--add']:
            db = dbc.add(db,args)
        elif command in ['-r','--rem']:
            db = dbc.remove(db,args)
        elif command in ['-g','--get']:
            dbc.retrieve(db,args)
        elif command in ['-l','--list']:
            dbc.list_keys(db)
            


if __name__=='__main__':
    main()