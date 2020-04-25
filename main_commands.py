import os
import vault
import getpass
from shell import db_shell
import shutil

def main_new(args):
    """Prompts for creating database"""
    while True:
        if not args:
            name = input('Vault Name: ')
        else:
            name = args[0]
        if os.path.isfile(vault.vault_file(name)):
            overwrite = input(f'Vault {name} already exists. Overwrite? [y/n]: ').lower()
            if overwrite!='y':
                return
        break
    while True:
        master_pwd = getpass.getpass('Master password (enter to abort): ')
        if not master_pwd:
            return
        master_pwd2 = getpass.getpass('Re-enter master password: ')
        if master_pwd!=master_pwd2:
            print('Passwords do not match!')
            continue
        break
    vault.new_db(name,master_pwd)
    db_shell(name,master_pwd)

def main_open(args):
    """Prompts for opening existing database"""
    while True:
        if not args:
            name = input('Vault Name: ')
        else:
            name = args[0]
        if not os.path.isfile(vault.vault_file(name)):
            print(f'No such vault: {name}')
            return
        break
    while True:
        master_pwd = getpass.getpass('Master password (enter to abort): ')
        if not master_pwd:
            return
        try:
            db_shell(name,master_pwd)
            break
        except ValueError:
            print('Incorrect password.')

def main_delete(args):
    """Delete a vault"""
    while True:
        if not args:
            name = input('Vault Name: ')
        else:
            name = args[0]
        if not os.path.isfile(vault.vault_file(name)):
            print(f'No such vault: {name}')
            return
        break
    while True:
        master_pwd = getpass.getpass('Master password (enter to abort): ')
        if not master_pwd:
            return
        
        try:
            vault.open_db(name,master_pwd)
        except ValueError:
            print('Incorrect password.')
            continue
        
        check = input(f'Are you sure you want to delete {name}? [y/n]: ').lower()
        if check=='y':
            shutil.rmtree(vault.vault_folder(name))
        return

def main_list():
    vaults = os.listdir(vault.VAULT_ROOT)
    vaults = [v for v in vaults if os.path.isdir(vault.vault_folder(v))]
    if vaults:
        for v in vaults:
            print(v)
    else:
        print('No vaults.')