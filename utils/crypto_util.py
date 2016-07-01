# !/usr/bin/python

"""
Program automatically detects what user user_input is and decrypts or
encrypts.

@author gold
@date   2012-08-10
"""

import sys
import csv
from CryptoManager import CryptoManager


def crypto(user_input):
    if user_input[0:4] == '\\x01':
        sans_token_input = user_input[4:]
        try:
            result = CryptoManager.decrypt(CryptoManager._PREFIX_TOKEN + sans_token_input)
        except Exception, e:
            result = 'ERROR: invalid user user_input'
    else:
        user_input = user_input.decode('utf-8')
        result = CryptoManager.encrypt(user_input)
        result = '\\x01' + result[1:]
    print result


def main():
    if len(sys.argv) != 2:
        print("""\n    USAGE: $ ./crypto_util.py "{plaintext|ciphertext|csvfile}"\n""")
        print("           If argument is ciphertext, you may need to quote the argument.\n")
        exit(1)

    target = sys.argv[1]
    if '.csv' in target:
        with open(target, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                crypto(row[0])
    else:
        crypto(target)

    exit(0)

if __name__ == '__main__':
    main()