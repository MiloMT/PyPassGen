"""Generates and stores a password or passwords given a set of parameters.

Using a series of CLI arguments and flags, this script will generate a
password or series of passwords seperate by new lines for user by the
user. The arguments allow which characters the password will use, and
how long each password will be. This module also uses the cryptography
library to encrypt password storage using a key generated by Fernet.

Typical Usage example:

    python __main__.py 10 5 -nsu
    python __main__.py 15 -sc

"""

import random
import sys
import string
import argparse
import pyperclip
# import re
# import cryptography

def seperator(func):
    
    def wrapper(*args):
        print("--------------------------------------------------")
        func(*args)
        
    return wrapper

@seperator
def pass_gen(args):
    
    password = ""
    pass_list = []
    char_list = [string.ascii_lowercase]
    
    # Flags to check for password character types
    if args.upper: char_list.append(string.ascii_uppercase)
    if args.number: char_list.append(string.digits)
    if args.special: char_list.append(string.punctuation)
    
    # Number of password to generate
    for _ in range(args.pass_num):  
        # Password generator dependent on char_num and arg flags
        for _ in range(int(args.char_num)):
            password += random.choice(random.choice(char_list))
        
        pass_list.append(password)
        password = ""
    
    # Copy passwords if flag entered
    if args.copy: pyperclip.copy("\n".join(pass_list))
    
    print("\n".join(pass_list))
    
    store_pass()

@seperator
def store_pass():
    # To do
    if args.save:
        # Check if passwords.txt already exists in current directory
        # If it does, ask whether to overwrite or append passwords
        # If not, say that file created
        confirmation = input("Placeholder")
        encrypt_pass()

@seperator
def encrypt_pass():
    # Ask whether to encrypt password txt file
    print("Testing")
    pass

@seperator
def retrieve_pass():
    # To do
    pass

def main():
    # To do
    pass

# Instantiate argparse
parser = argparse.ArgumentParser(
    description="Generates a password or series of passwords given a "
    "set of parameters"
    )

# List of positional arguments
parser.add_argument("char_num", metavar="Num_of_Chars",  
                    type=int, help="Number of characters in password.")
parser.add_argument("pass_num", metavar="Num_of_Passwords", 
                    nargs="?", default=1, type=int, 
                    help="Optionally create a number of passwords. (default: 1)")
parser.add_argument("regex", metavar="Regular_Expression", nargs="?", 
                    default=None, type=str, help="Optionally create a regular "
                    "expression for password generation.")

# List of options
parser.add_argument("-c", "--copy", help="Copies the password to the "
                    "clipboard once generated", action="store_true")
parser.add_argument("-H", "--hide", help="Stops the password from printing "
                    "to CLI", action="store_true")
parser.add_argument("-n", "--number", help="Adds numbers to password generation",
                    action="store_true")
parser.add_argument("-s", "--special", help="Adds special characters to "
                    "password generation", action="store_true")
parser.add_argument("--save", help="Saves password/s in a txt file in CWD "
                    "called 'passwords.txt'", action="store_true")
parser.add_argument("-u", "--upper", help="Adds uppercase letters to "
                    "password generation", action="store_true")

# Parse the passed arguments
args = parser.parse_args()

print("\nPasswords Generated:")
pass_gen(args)

if __name__ == "__main__":
    main()