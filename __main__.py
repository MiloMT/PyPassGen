"""Generates and stores a password or passwords given a set of parameters.

Using a series of CLI arguments and flags, this script will either generate 
a password or series of passwords seperate by new lines for user by the
user, or view either a plain txt file or encrypted text file and print
the results. The arguments allow which characters the password will use, and
how long each password will be. This module also uses the cryptography
library to encrypt password storage using a key generated by Fernet. Lastly,
The user can choose to create a custom expression to dictate the generation
of the password.

Typical Usage example:

    python __main__.py 10 5 -nsu
    python __main__.py 15 -sc
    python __main__.py --view
"""

import random
import string
import argparse
import os

import pyperclip

from cryptography.fernet import Fernet


def arg_check(
    var: string,
    arg1: string,
    arg1_desc: string,
    arg2: string,
    arg2_desc: string,
) -> string:
    """Error checking when receiving user input arguments.

    Retrieves multiple arguments depending on input check required
    and prints relevant output message if input isn't as expected.
    Provides user with relevant descriptors for getting new input.

    Args:
        var: The variable to check expected results against.
        arg1: First option as a single character.
        arg1_desc: Extended version of the first character.
        arg2: Second option as a single character.
        arg2_desc: Extended version of the second character.

    Returns:
        If variable is cleared, returns unchanged, otherwise will
        repeatedly ask for user input until inputted argument
        matches expected argument.

    Raises:
        ValueError: An error if value isn't as expected. Note: Not yet
        implemented.
    """

    while var not in (arg1, arg2):
        var = (
            input(
                f"Sorry, but that wasn't a valid input. Please enter"
                f"a [{arg1.upper()}] for {arg1_desc} or [{arg2.upper()}] "
                f"for {arg2_desc}: ",
            )
            .lower()
            .strip()
        )

    return var


def pass_gen(arguments: object, expression: string = None) -> list:
    """Password generator function.

    Generates password based on flags and expression (if
    any provided). Flags are passed and checked.

    Args:
        arguments: Object containing parsed CLI arguments.
        expression: An user created expression that dictates
            how a password is generated.

    Returns:
        A list of generated passwords.
    """

    password: str = ""
    pass_list: list = []
    char_list: list = [string.ascii_lowercase]

    # Flags to check for password character types.
    if arguments.upper:
        char_list.append(string.ascii_uppercase)
    if arguments.number:
        char_list.append(string.digits)
    if arguments.special:
        char_list.append(string.punctuation)

    if expression is not None:
        # Number of password to generate.
        for _ in range(arguments.pass_num):
            # Password generator dependent on expression.
            for x in expression:
                match x:
                    case "l":
                        password += random.choice(string.ascii_lowercase)
                    case "u":
                        password += random.choice(string.ascii_uppercase)
                    case "n":
                        password += random.choice(string.digits)
                    case "s":
                        password += random.choice(string.punctuation)

            pass_list.append(password)
            password = ""
    else:
        # Number of password to generate.
        for _ in range(arguments.pass_num):
            # Password generator dependent on char_num and arg flags.
            for _ in range(int(arguments.char_num)):
                password += random.choice(random.choice(char_list))

            pass_list.append(password)
            password = ""

    # Copy passwords if flag entered.
    if arguments.copy:
        pyperclip.copy("\n".join(pass_list))

    # Formatted password printing
    print("--------------------------------------------------")
    print("\n".join(pass_list))
    print("--------------------------------------------------")

    return pass_list


def store_pass(arguments: object, pass_list: list) -> None:
    """Password storage in text files.

    Receives a list of passwords and than proceeds to write
    those passwords to a file called 'passwords.txt' within
    the current directory. User can choose to overwrite or
    append passwords if the file already exists.

    Args:
        arguments: Object containing parsed CLI arguments.
        pass_list: List of generated passwords.
    """

    # Check if passwords.txt already exists in current directory.
    if os.path.isfile("passwords.txt"):
        # If it does, ask whether to overwrite or append passwords.
        print("There is already a passwords file in the current directory.")
        write_type = input(
            "Would you like to overwrite the file or append to "
            "this file? [W] or [A]: "
        )
        write_type = arg_check(write_type, "w", "overwrite", "a", "append")
        # Ask user to confirm overwrite as long as force option wasn't used.
        if write_type == "w" and not arguments.force:
            overwrite_confirm = (
                input(
                    "This will overwrite your existing password file "
                    "resulting in the current passwords being lost, "
                    "are you sure? [Y] or [N]: "
                )
                .lower()
                .strip()
            )
            overwrite_confirm = arg_check(
                overwrite_confirm, "y", "yes", "n", "no"
            )

        # Checks if force flag used or if user has confirmed overwrite.
        if write_type == "a" or arguments.force or overwrite_confirm == "y":
            with open("passwords.txt", write_type, encoding="UTF-8") as f:
                # Add extra line to list if appending
                if write_type == "a":
                    f.write("\n")
                f.write("\n".join(pass_list))
        else:
            # Rerun save function if confirmation is denied
            store_pass(arguments, pass_list)
    else:
        # If passwords.text doesn't exist, automatically create file.
        with open("passwords.txt", "w", encoding="UTF-8") as f:
            f.write("\n".join(pass_list))
        print(
            "Your passwords have been saved in the 'passwords.txt'",
            "file in the current directory",
        )


def encrypt_pass() -> None:
    """Encrypting stored passwords.

    Encrypts passwords stored in 'passwords.txt' based off either
    new or existing key. If a new key is generated, the key is
    stored in a file called 'key.txt' in the current directory. If
    the 'key.txt' file already exists, then the key in that file is
    used.
    """

    # Check whether there is already an active key present
    if os.path.isfile("key.txt"):
        with open("key.txt", "r", encoding="UTF-8") as f:
            key = f.read()

    else:
        # Generate a key and save it if none available
        key = Fernet.generate_key()
        with open("key.txt", "wb") as f:
            f.write(key)

        print(
            "A new key has been created in the current directory as 'key.txt'."
            " Keep this safe!"
        )
    # Create fernet object from key from cryptography library
    fernet = Fernet(key)
    # Take passwords from current file, this means that if there is
    # already a password list, it can encrypt pre-existing files
    with open("passwords.txt", "r+", encoding="UTF-8") as f:
        data = f.read()
    # Encrypt password list into a byte object for encryption
    with open("passwords.txt", "wb") as f:
        token = fernet.encrypt(data.encode("utf-8"))
        f.write(token)


def retrieve_pass() -> None:
    """Retrieving passwords and printing on screen.

    Retrieves passwords from 'passwords.txt' file if it exists.
    Also checks whether a key exists for encrypted passwords, and
    if so, will decrypt the password prior to printing out. Also
    has the ability to copy the passwords from an existing file.
    """

    if os.path.isfile("passwords.txt"):
        # Checks if encryption has been used
        if os.path.isfile("key.txt"):
            with open("key.txt", "r", encoding="UTF-8") as f:
                key = f.read()

            with open("passwords.txt", "r", encoding="UTF-8") as f:
                token = f.read()

            # Generates fernet object from existing key and
            # decrypts passwords file
            fernet = Fernet(key)
            pass_list = fernet.decrypt(token).decode("UTF-8").split("\n")
        else:
            # Otherwise if no key.txt file exists, read passwords as per normal
            with open("passwords.txt", "r", encoding="UTF-8") as f:
                data = f.read()
                pass_list = data.split("\n")

        # If copy flag used, copies pass_list from file
        if args.copy:
            pyperclip.copy("\n".join(pass_list))

        # Formatted password display
        print("Passwords in passwords.txt:")
        print("--------------------------------------------------")
        for password in pass_list:
            print(password)
        print("--------------------------------------------------")

    else:
        print("There is no password.txt file in the current directory.")


def expression_gen() -> string:
    """Generates an expression to be used to dictate password generation.

    Provides a list of instructions to the user to assist in generating
    a user defined expression for password generation. Provided with
    a list of characters, the user can create a non-determined password
    length as dictated by the letters used.

    Returns:
        An error checked expression to be used for password generation.

    Raises:
        ValueError: An error if one of the chars isn't expected. Note: Not
        yet implemented.
    """

    invalid_chars: list = []

    print(
        "You've selected to create an expression to use for password "
        "generation.\nA password expression is created by using a sequence of "
        "characters in a\ndesignated order. The characters to use are below:"
        "\n\n - [L] lowercase letter\n - [U] uppercase letter\n - [N] digit\n -"
        " [S] special character\n\nPlease refer to the github repo for "
        "expression examples.\n"
    )
    expression = (
        input("Please input a compatible expression: ").lower().replace(" ", "")
    )

    while True:
        # Checks for if any characters in expression are invalid.
        for x in expression:
            if x not in ("l", "u", "n", "s"):
                invalid_chars.append(x)
        # Breaks out of check if no invalid characters
        if len(invalid_chars) == 0:
            break
        # Lets user know which characters are invalid
        print(
            "\nYour expression is not valid. The invalid characters are:\n\n - "
            f"{"\n - ".join(invalid_chars)}\n"
        )
        invalid_chars = []
        expression = (
            input("Please try to input another expression: ")
            .lower()
            .replace(" ", "")
        )

    return expression


def main(arguments: object) -> None:
    """PyPassGen main functionality.

    If this is the main module, runs the standard PyPassGen functionality.
    Checks flags and runs appropriately. If view mode selected, than
    will ignore all generation capability. Otherwise, will check whether
    the expression functionality was chosen first, than will generate
    password depending on result, lastly will check if user wants to save
    and than encrypt passwords to the local directory.

    Args:
        arguments: Object containing parsed CLI arguments.
    """

    # If view mode, ignore generator
    if arguments.view:
        retrieve_pass()
    else:
        # Check if expression generation used first to pass expression
        if arguments.expression:
            expression = expression_gen()
            print("\nPasswords Generated:")
            pass_list = pass_gen(arguments, expression)
        else:
            print("Passwords Generated:")
            pass_list = pass_gen(arguments)

        # Prompts user to check if they want to save.
        save_confirm = (
            input(
                "Would you like to save your generated passwords? [Y] or [N]: "
            )
            .lower()
            .strip()
        )
        save_confirm = arg_check(save_confirm, "y", "yes", "n", "no")

        if save_confirm == "y":
            store_pass(arguments, pass_list)
            # Checks for encryption if user has prompted to save
            encrypt_confirm = (
                input(
                    "Would you like to encrypt your saved passwords?"
                    "[Y] or [N]: "
                )
                .lower()
                .strip()
            )
            encrypt_confirm = arg_check(encrypt_confirm, "y", "yes", "n", "no")

            if encrypt_confirm == "y":
                encrypt_pass()


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
        nargs="?",
        default=10,
        type=int,
        help="Optionally enter a number of characters in password. (default: 10)",
    )
    parser.add_argument(
        "pass_num",
        metavar="Num_of_Passwords",
        nargs="?",
        default=1,
        type=int,
        help="Optionally create a number of passwords. (default: 1)",
    )

    # List of options
    parser.add_argument(
        "-c",
        "--copy",
        help="Copies the password to the clipboard once generated or viewed",
        action="store_true",
    )
    parser.add_argument(
        "-e",
        "--expression",
        help="Lets the generator know that you want to create an"
        " expression to control the password generation",
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
    parser.add_argument(
        "--view",
        help="Instead of generating passwords, prints out passwords to terminal",
        action="store_true",
    )

    # Parse the passed arguments
    args = parser.parse_args()

    main(args)
