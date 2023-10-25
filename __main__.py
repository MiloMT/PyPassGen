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
import os

# import re
# import cryptography


def arg_check(
    var: string, arg1: string, arg1_desc: string, arg2: string, arg2_desc: string
) -> string:
    while var not in (arg1, arg2):
        var = input(
            f"Sorry, but that wasn't a valid input. Please enter"
            f"a [{arg1.upper()}] for {arg1_desc} or [{arg2.upper()}] "
            f"for {arg2_desc}: ",
        ).lower()

    return var


def pass_gen(args: object, regex: string = None) -> list:
    password = ""
    pass_list = []
    char_list = [string.ascii_lowercase]

    # Flags to check for password character types.
    if args.upper:
        char_list.append(string.ascii_uppercase)
    if args.number:
        char_list.append(string.digits)
    if args.special:
        char_list.append(string.punctuation)

    # Number of password to generate.
    for _ in range(args.pass_num):
        # Password generator dependent on char_num and arg flags.
        for _ in range(int(args.char_num)):
            password += random.choice(random.choice(char_list))

        pass_list.append(password)
        password = ""

    # Copy passwords if flag entered.
    if args.copy:
        pyperclip.copy("\n".join(pass_list))

    print("--------------------------------------------------")
    print("\n".join(pass_list))
    print("--------------------------------------------------")

    return pass_list


def store_pass(args: object, pass_list: list) -> bool:
    # Check if passwords.txt already exists in current directory.
    if os.path.isfile("passwords.txt") == True:
        # If it does, ask whether to overwrite or append passwords.
        print("There is already a passwords file in the current directory.")
        write_type = input(
            "Would you like to overwrite the file or append to "
            "this file? [W] or [A]: "
        )
        write_type = arg_check(write_type, "w", "overwrite", "a", "append")
        # Ask user to confirm overwrite as long as ignore option wasn't used.
        if write_type == "w" and args.force == False:
            overwrite_confirm = input(
                "This will overwrite your existing"
                " password file, are you sure? [Y] or [N]: "
            ).lower()
            overwrite_confirm = arg_check(overwrite_confirm, "y", "yes", "n", "no")

        # Checks if force flag used or if user has confirmed overwrite.
        if overwrite_confirm == "y" or args.force == True:
            with open("passwords.txt", write_type) as f:
                if write_type == "a":
                    f.write("\n")
                f.write("\n".join(pass_list))
            # Bool value for whether passwords were saved or not
            return True
        else:
            print("Save aborted")
            # Bool value for whether passwords were saved or not
            return False
    else:
        # If passwords.text doesn't exist, automatically create file.
        with open("passwords.txt", "w") as f:
            f.write("\n".join(pass_list))
        print(
            "Your passwords have been saved in the 'passwords.txt'",
            "file in the current directory",
        )
        # Bool value for whether passwords were saved or not
        return True


def encrypt_pass(args: object, pass_list: list) -> None:
    # Ask whether to encrypt password txt file
    print("Testing")
    pass


def retrieve_pass():
    # To do
    pass


def regex_gen() -> string:
    pass


def main(args):
    if args.regex == True:
        regex = regex_gen()
        print("Passwords Generated:")
        pass_list = pass_gen(args, regex)
    else: 
        print("Passwords Generated:")
        pass_list = pass_gen(args)
        
    save_confirm = input(
        "Would you like to save your generated passwords? [Y] or [N]: "
    ).lower()
    save_confirm = arg_check(save_confirm, "y", "yes", "n", "no")

    if save_confirm == "y":
        is_saved = store_pass(args, pass_list)

    # Only asks to encrypt is passwords were saved
    if is_saved == True:
        encrypt_confirm = input(
            "Would you like to encrypt your saved passwords? [Y] or [N]: "
        ).lower()
        encrypt_confirm = arg_check(encrypt_confirm, "y", "yes", "n", "no")

        if encrypt_confirm == "y":
            encrypt_pass(args, pass_list)


if __name__ == "__main__":
    # Instantiate argparse
    parser = argparse.ArgumentParser(
        description="Generates a password or series of passwords given a "
        "set of parameters"
    )

    # List of positional arguments
    parser.add_argument(
        "char_num",
        metavar="Num_of_Chars",
        type=int,
        help="Number of characters in password.",
    )
    parser.add_argument(
        "pass_num",
        metavar="Num_of_Passwords",
        nargs="?",
        default=1,
        type=int,
        help="Optionally create a number of passwords. (default: 1)",
    )
    parser.add_argument(
        "regex",
        metavar="Regular_Expression",
        nargs="?",
        default=False,
        type=str,
        help="Optionally create a regular expression for password generation."
        " (default: False)",
    )

    # List of options
    parser.add_argument(
        "-c",
        "--copy",
        help="Copies the password to the clipboard once generated",
        action="store_true",
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Forces overwrite so app ignores overwrite confirmation",
        action="store_true",
    )
    parser.add_argument(
        "-n",
        "--number",
        help="Adds numbers to password generation",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--special",
        help="Adds special characters to password generation",
        action="store_true",
    )
    parser.add_argument(
        "-u",
        "--upper",
        help="Adds uppercase letters to password generation",
        action="store_true",
    )

    # Parse the passed arguments
    args = parser.parse_args()

    main(args)