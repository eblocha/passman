import secrets
from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
import os
from Cryptodome.Random import get_random_bytes
import json

def encrypt_master(master_key,master_pwd):
    """Encrypt a master key with AES using the master password"""
    salt = get_random_bytes(8)
    secondary = hashlib.pbkdf2_hmac('sha256',master_pwd.encode(),salt,2**14,16)
    cipher_config = AES.new(secondary,AES.MODE_EAX)
    cipher_text, tag = cipher_config.encrypt_and_digest(master_key)
    return {
        'cipher_text': cipher_text,
        'salt': salt,
        'tag': tag,
        'nonce': cipher_config.nonce
    }

def generate_keys(master_pwd):
    """Generate a new master key and encrypt it with a master password"""
    master = get_random_bytes(32)
    return master, encrypt_master(master,master_pwd)

def decrypt_master(master_pwd,master_dict):
    """Decrypt a master key with a master password"""
    secondary = hashlib.pbkdf2_hmac('sha256',master_pwd.encode(),master_dict['salt'],2**14,16)
    cipher = AES.new(secondary,AES.MODE_EAX,nonce=master_dict['nonce'])
    master = cipher.decrypt_and_verify(master_dict['cipher_text'], master_dict['tag'])
    return master

def encrypt_file(text,master_pwd,master_key):
    """Encrypt a database file with the master key"""
    cipher_file = AES.new(master_key,AES.MODE_GCM)
    cipher_text, tag = cipher_file.encrypt_and_digest(bytes(text, 'utf-8'))
    return {
        'cipher_text': cipher_text,
        'nonce': cipher_file.nonce,
        'tag': tag
    }

def decrypt_file(cipher_d_file,master_pwd,master_key):
    """Decrypt a database file with the master key"""
    cipher_file = AES.new(master_key,AES.MODE_GCM,nonce=cipher_d_file['nonce'])
    return json.dumps(cipher_file.decrypt_and_verify(cipher_d_file['cipher_text'], cipher_d_file['tag']))

def write_file(name,db,master_pwd,master_key):
    """Encrypt and write a database to disk"""
    db_cipher = encrypt_file(json.dumps(db),master_pwd,master_key)
    db_file = {key: b64encode(db_cipher[key]).decode('utf-8') for key in db_cipher}
    with open(f'{name}.json','w') as f:
        json.dump(db_file,f)

def new_db(name,master_pwd):
    """Initialize a new database master key and file"""
    master_key, master_dict = generate_keys(master_pwd)
    master_file = {key: b64encode(master_dict[key]).decode('utf-8') for key in master_dict}
    with open(f'{name}_master.json','w') as f:
        json.dump(master_file,f)
    db = dict()
    write_file(name, db, master_pwd, master_key)

def open_db(name,master_pwd):
    """Open and decrypt a database"""
    with open(f'{name}_master.json','r') as f:
        master_file = json.load(f)
    with open(f'{name}.json','r') as f:
        db_file = json.load(f)
    
    master_dict = {key: b64decode(master_file[key]) for key in master_file}
    db_cipher = {key: b64decode(db_file[key]) for key in db_file}

    return decrypt_file(db_cipher,master_pwd,master_dict), decrypt_master(mster_pwd, master_dict)

def retrieve(db):
    """Retrieve values from the database"""
    return {key: db[key] for key in keys}

def add(db,updates):
    """Add new values to the database, then re-encrypt and save"""
    db.update(updates)
    return db

def remove(name,master_pwd,keys):
    """Remove values from the database, then re-encrypt and save"""
    for key in keys:
        del db[key]
    return db

def list_keys(name,master_pwd):
    """List all keys existing in the database"""
    return list(db.keys())

def change_master(name,master_pwd,new_master_pwd):
    """Change the master password and re-encrypt the master key"""
    with open(f'{name}_master.json','r') as f:
        master_file = json.load(f)
        master_dict = {key: b64decode(master_file[key]) for key in master_file}

    master = decrypt_master(master_pwd,master_dict)
    new_master_dict = encrypt_master(master,new_master_pwd)
    master_file = {key: b64encode(master_dict[key]).decode('utf-8') for key in master_dict}
    with open(f'{name}_master.json','w') as f:
        json.dump(master_file,f)


if __name__=='__main__':
    add('v','abc123;?','facebook.com',{'username':'hello','password':'xyz098'})
    print(retrieve('v','abc123;?','google.com'))
    print(retrieve('v','abc123;?','facebook.com'))