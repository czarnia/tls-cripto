import sys
sys.path.append('../')

from common.string_socket import StringSocket

def main():
	skt = StringSocket()
	
	skt.bind('0.0.0.0', 8080)
	skt.listen(1)
	print("Soy el servidor y estoy escuchando conexiones")

	request_skt, addr = skt.accept()

	print(f"Soy el servidor y acepte una conexion de: {addr}")
	print("Soy el servidor y voy a enviar")

	request_skt.send_with_size("Hola cliente!")

	msg = "hola"
	while (msg!=b'0'.hex()):
		msg = request_skt.receive_with_size()
		print(f"Soy el servidor y recibi: {bytes.fromhex(msg)}")

	request_skt.close()
	skt.close()

if __name__ == '__main__':
	main()
