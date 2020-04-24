"""Provide a shell to interact with databases"""
import vault

commands = {
    '--new': vault.new_db,
    '--open': vault.open_db
}

def main():
    """Main shell routine to work with multiple databases"""

def db_shell(name,master_pwd):
    """Initialize a new shell inside the given DB with the given master password"""
    db, master_key = vault.open_db(name,master_pwd)
    while True:
        command = input(f'({name}) >>> ')
        args = command.split(' ')
        commands = {
            '--add': vault.add,
            '--remove': vault.remove,
            '--get': vault.retrieve,
            '--list': vault.list_keys,
            '--exit': vault.write_file,
        }