"""
 File: Encryption.py
 Authors: Leah Hadeed
          Nazariy Gunko

 Description:
 
 This script is in charge of all crypto-security aspects of the project.
 It controls the encryption, decryption, and signing of files through the
 use of public and private keys, as per cryptographical theory.
"""

# Python Libraries
import json
import os
import sys

# Cryptographic libraries 
from Crypto.PublicKey       import RSA
from Crypto.Cipher          import AES, PKCS1_OAEP
from Crypto.Random          import get_random_bytes
from Crypto.Util.Padding    import pad, unpad
from Crypto.Signature       import pkcs1_15
from Crypto.Hash            import SHA256

# Printing arguments
from ..Colours import Colours

# This class acts as an encryption/decryption and signature tool
class Encryption:
    authorization = ''
    colours = None

    # Constructor for class
    def __init__(self, authorization):
        self.authorization = authorization
        self.colours = Colours()

    def print_error(self, string):
        print(self.colours.cyan('->') + self.colours.red(' ERROR: ') + string)

    def print_ok(self, string):
        print(self.colours.cyan('->') + string + self.colours.green('OK'))


    # Function that encrypts a given file
    def encrypt(self, filename, user_public_key):
        # Error control: Opening File
        try:
            # Open file in binary mode
            file = open(filename, "rb")
            # Read file
            content = file.read()
        # Case: Non-existent file
        except:
            self.print_error('File: ' + self.colours.red(filename) + ' not found.')
            return

        # AES Key
        aKey = get_random_bytes(32)
        # iv
        sKey = get_random_bytes(16)
        # Get publicKey of the receiver
        pKey = RSA.import_key(user_public_key)
        # Create the digital pack
        enc = PKCS1_OAEP.new(pKey)
        pack = enc.encrypt(aKey)
        # Encrypt the data
        aes_enc = AES.new(aKey, AES.MODE_CBC, sKey)
        result_data = aes_enc.encrypt(pad(content, 16))

        # Generate the encrypted file
        file.close()
        res_file = open(filename, "wb")
        for x in (sKey, pack, result_data):
            res_file.write(x)

        res_file.close()
        return

    # Function that signs a file
    def sign(self, filename):

        # Error control: Opening File
        try:
            # Open file in binary mode
            file = open(filename, "rb")
            # Read file
            content = file.read()
        # Case: Non-existent file
        except:
            self.print_error('File: ' + self.colours.red(filename) + ' not found.')
            return

        # Get private key from .PEM file
        pKey = RSA.import_key(open('private.pem').read())
        # Generate hash of content
        hash = SHA256.new(content)
        # Sign key
        sign = pkcs1_15.new(pKey).sign(hash)

        # Close file descriptor
        file.close()

        # Open file for signing
        res_file = open(filename, "wb")
        for x in (sign, content):
            res_file.write(x)

        # Close file descriptor
        res_file.close()

        # Print intermediate status message
        self.print_ok(' Signing file...')
        return


    # Function that signs and encrypts a file
    def sign_encrypt(self, filename, user_public_key):

        try:
            # First we sign the file using the function we defined beforehand
            self.sign(filename)
        except:
            self.print_error(' Signing error.')
            return

        try:
            # Next we encrypt the file
            self.encrypt(filename, user_public_key)
        except:
            self.print_error(' Encryption error.')
            return

        self.print_ok(' Signature and Encryption...')


    # Check wether a sign is valid
    def validate_sign(self, signature, message, user_pk):
        # Import the public key of the given user
        pKey = RSA.import_key(user_pk)
        # Creating a hash of the given message
        h = SHA256.new(message)

        # Test for valid signature
        try:
            # Verify the validity of message and signature
            pkcs1_15.new(pKey).verify(h, signature)
            self.print_ok(' Verifying signature...')

        # Case: Signature Invalid
        except:
            self.print_error(' Signature validation error.')
            return False

        return True


    # Function that unencrypts a given file
    # Set signed to True if the file has been signed, False otherwise
    def decryptFile(self, filename, user_pk, signed):
        # Error Control: Opening File
        try:
            # Open file in binary mode
            file = open(filename, "rb")
            # Read content
            content = file.read()
        # Case: Non-existent file
        except:
            print("File: " + Colours.Colours.red(filename) + " not found.")
            return

        # Get the values
        iv = content[:16]
        pack = content[16:272]
        text = content[272:]

        # Get the key by unencrypting the digital pack with RSA
        private_key = RSA.import_key(open("private.pem").read())
        enc = PKCS1_OAEP.new(private_key)
        key = enc.decrypt(pack)
        # Unencrypt the sign and message using the AES key and iv
        cipher = AES.new(key, AES.MODE_CBC, iv)
        final_message = unpad(cipher.decrypt(text), 16)

        # Close file descriptor
        file.close()

        # Test for signature
        if signed:
            # Test validity of signature
            valid = self.validate_sign(final_message[:256], final_message[256:], user_pk)

            if valid:
                # Write back the result
                res_file = open(filename, "wb")
                res_file.write(final_message[256:])
                return
            # Case: Signature Invalid
            else:
                self.print_error(' Invalid Signature.')
                return
        else:
            res_file = open(filename, "wb")
            res_file.write(final_message)
            return

        self.print_ok('Decryption Success...')
        return
