import pytest
import argparse
import string
import os
import main

import pyperclip

from cryptography.fernet import Fernet

def test_passgen():
    """Tests pass_gen function
    
    Runs a test with an example set of parameters to check that the pass_gen
    function works as expected. A series of arguments are fed in to ensure that
    both the length of the passwords and the amount of passwords match the
    expected output. 2 Variations are used to test this.
    """
    
    # First variation
    # ====================
    # Need to generate argparse object
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    # Instantiate explicit argparse attributes
    args.upper = True;
    args.number = True;
    args.special = True;
    args.pass_num = 5;
    args.char_num = 10;
    args.copy = False;
    
    pass_list = main.pass_gen(args)
    
    # Check if amount of passwords is correct
    assert len(pass_list) == 5
    
    password_length = True
    # Check if length of any passwords in list is incorrect
    for password in pass_list:
        assert len(password) == 10
        
    # Second variation
    # ====================
    # Need to generate argparse object
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    # Instantiate explicit argparse attributes
    args.upper = True;
    args.number = True;
    args.special = True;
    args.pass_num = 2;
    args.char_num = 50;
    args.copy = False;
    
    pass_list = main.pass_gen(args)
    
    # Check if amount of passwords is correct
    assert len(pass_list) == 2
    
    password_length = True
    # Check if length of any passwords in list is incorrect
    for password in pass_list:
        assert len(password) == 50

def test_store_pass():
    """Tests store_pass function
    
    Runs a test with an example set of parameters to check that the store_pass
    function works as expected. The expected outputs are that a passwords.txt
    file gets created and that the contents match the "Test Password" that we
    feed in.
    """
    
    # Need to generate argparse object
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    # Instantiate explicit argparse attributes
    args.force = True
    # Instantiate sample password list
    pass_list = ["TestPassword"]
    # Remove password file if existing
    if os.path.isfile("passwords.txt"):
        os.remove("passwords.txt")
    
    main.store_pass(args, pass_list)
    
    # Check whether a passwords.txt file was created
    assert os.path.isfile("passwords.txt")
        
    with open("passwords.txt", "r") as f:
        data = f.read()
    # Check if the contents of file are expected
    assert data == "TestPassword"
    
    # Clear out test files
    os.remove("passwords.txt")

def test_encrypt_pass(capfd):
    """Tests encrypt_pass & retrieve_pass functions
    
    Runs a test with an example set of parameters to check that the encrypt_pass
    function works as expected and than the retrieve_pass function can
    successfully decrypt the encrypted passwords.txt file. The expected outputs 
    are that a key.txt file is created. And that the print statements match
    the correctly decrypted password.
    """
    
    # Remove passwords.txt if already existing
    if os.path.isfile("passwords.txt"):
        os.remove("passwords.txt")
    
    # Need to create an example passwords.txt file
    with open("passwords.txt", "w") as f:
        f.write("Test Password")
    
    main.encrypt_pass()
    
    # Ensure a key was created.
    assert os.path.isfile("key.txt")
    
    with open("passwords.txt", "r") as f:
        data = f.read()
        
    # Ensure passwords.txt has been encrypted
    assert data != "Test Password"
    
    # Need to generate argparse object
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    # Instantiate explicit argparse attributes
    args.copy = False
    
    main.retrieve_pass(args)
    
    # Check for printed text
    out, err = capfd.readouterr()
    assert "Test Password" in out
    
    # Clear out test files
    os.remove("passwords.txt")
    os.remove("key.txt")