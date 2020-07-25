'''This PoC uses the Poodle attack - PoC of mpgn <martial.puygrenier@gmail.com>'''

import binascii
import sys
import hmac, hashlib
from Crypto.Cipher import AES
from Crypto import Random

import sys
sys.path.append('../')

from common.string_socket import StringSocket

SECRET = "auth:CRIPTO2020"
LENGTH_BLOCK = 16

# generate random value for keys and ivs
def randkey():
    return Random.new().read(AES.block_size)

# padding for the CBC cipher block
def pad(s):
    return (16 - len(s) % 16) * chr((16 - len(s) - 1) % 16)

# cipher a message
def encrypt(msg, key, iv):
    data = msg.encode()
    hash = hmac.new(key, data, hashlib.sha256).digest()
    padding = pad(data + hash)
    raw = data + hash + padding.encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(raw)

def main():
	skt = StringSocket()

	skt.connect("server", 8080)
	print("Soy el cliente y me conecté.")

	# fill the last block with full padding 0f
	key = randkey()
	iv = randkey()
	t = binascii.hexlify(encrypt(SECRET, key, iv))
	original_length = len(t)

	t = 1
	while True:
		length = len(binascii.hexlify(encrypt("a"*t + SECRET, key, iv)))
		if(length > original_length):
			break
		t += 1

	# we can decipher block_1...block_n-2 => the plaintext
	for block in range(original_length//32-2,0,-1):
		for char in range(LENGTH_BLOCK):
			while True:
				key = randkey()
				iv = randkey()

				# Sending the encripted block
				skt.send_with_size(binascii.hexlify(encrypt("$"*16 + "#"*t + SECRET + "%"*(block*LENGTH_BLOCK - char), key, iv)).hex())
				# Sending the iv and key to simulate if the server accepts the packets or not
				skt.send_with_size(iv.hex())
				skt.send_with_size(key.hex())

				msg = skt.receive_with_size()
				if (msg == "Adivinado"):
					print ("Sigo enviando según pedido.")
					t += 1
					break
	skt.close()

if __name__ == '__main__':
	main()
