'''This PoC uses the Poodle attack - PoC of mpgn <martial.puygrenier@gmail.com>'''

import binascii
import sys
import hmac, hashlib
from Crypto.Cipher import AES
from Crypto import Random

import sys
sys.path.append('../')

from common.string_socket import StringSocket

IV = Random.new().read( AES.block_size )
KEY = Random.new().read( AES.block_size )

# generate random key and iv
def randkey():
    global IV 
    IV = Random.new().read( AES.block_size )
    global KEY 
    KEY = Random.new().read( AES.block_size )

# padding for the CBC cipher block
def pad(s):
    return (16 - len(s) % 16) * chr((16 - len(s) - 1) % 16)

# cipher a message
def encrypt( msg):
    data = msg.encode()
    hash = hmac.new(KEY, data, hashlib.sha256).digest()
    padding = pad(data + hash)
    raw = data + hash + padding.encode()
    cipher = AES.new(KEY, AES.MODE_CBC, IV )
    return cipher.encrypt( raw )

def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]

def main():
	skt = StringSocket()

	skt.connect("server", 8080)
	print("Soy el cliente y me conecté.")

	msg = ""

	SECRET = "CRIPTOFIUBA2020"

	secret = []

	length_block = 16

	a = encrypt(SECRET)

	# fill the last block with full padding 0f
	t = binascii.hexlify(encrypt(SECRET))
	original_length = len(t)
	t = 1
	while(True):
		length = len(binascii.hexlify(encrypt("a"*t + SECRET)))
		if( length > original_length ):
			break
		t += 1
	save = t
	v = []

	# we can decipher block_1...block_n-2 => the plaintext
	for block in range(original_length//32-2,0,-1):
		for char in range(length_block):
			count = 0
			while True:
				randkey()
				request = split_len(binascii.hexlify(encrypt("$"*16 + "#"*t + SECRET + "%"*(block*length_block - char))), 32)
				# Envío el bloque encriptado
				skt.send_with_size(binascii.hexlify(encrypt("$"*16 + "#"*t + SECRET + "%"*(block*length_block - char))).hex())
				# Envío el initializator para luego simular si el server "acepta" el paquete o no.
				skt.send_with_size(IV.hex())
				# Envío la clave para luego simular si el server "acepta" el paquete o no.
				skt.send_with_size(KEY.hex())

				msg = skt.receive_with_size()
				if (msg == "Adivinado"):
					print ("Sigo enviando.")
					t += 1
					break
	skt.close()

if __name__ == '__main__':
	main()
