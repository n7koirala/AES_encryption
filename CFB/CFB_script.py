#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time
from base64 import b64decode
from Crypto.Util.Padding import pad,unpad


class Encryptor:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, message, key, key_size=256):
        #message = self.pad(message)
        padded_bytes = pad(message, AES.block_size)
        AES_obj = AES.new(key, AES.MODE_CFB, iv)
        ciphertext = AES_obj.encrypt(padded_bytes)
        return ciphertext

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        AES_obj = AES.new(key, AES.MODE_CFB, iv)
        raw_bytes = AES_obj.decrypt(ciphertext)
        plaintext = unpad(raw_bytes, AES.block_size)
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'CFB_script.py' ): # name of the file to be put here
                    dirs.append(dirName + "//" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)


key = pad(b"keycanbeputhere", AES.block_size)
iv = pad(b"ivcanbeputhere", AES.block_size)
enc = Encryptor(key, iv)
clear = lambda: os.system('cls')

def main():
    while True:
        clear()
        choice = int(input(
            " Select an option: \n1 -> Encrypt single file\n2 -> Decrypt single file\n3 -> Encrypt all files in the curr folder\n4 -> Decrypt all files in the curr folder\n5 -> Quit\n"))
        clear()
        if choice == 1:
            enc.encrypt_file(str(input("Enter name of file to encrypt: ")))
        elif choice == 2:
            enc.decrypt_file(str(input("Enter name of file to decrypt: ")))
        elif choice == 3:
            start = time.time()
            enc.encrypt_all_files()
            end = time.time()
            print("Took " + str(end - start) + " seconds to encrypt!")
        elif choice == 4:
            start = time.time()
            enc.decrypt_all_files()
            end = time.time()
            print("Took " + str(end - start) + " seconds to decrypt!")
        elif choice == 5:
            exit()
        else:
            print("Please select a valid option!")

if __name__ == "__main__":
    main()
