import sys
sys.path.append('../')

from common.string_socket import StringSocket

def main():
	skt = StringSocket()

	skt.connect("server", 8080)
	print("Soy el cliente y me conecte al servidor")

	msg = skt.receive_with_size()
	print(f"Soy el cliente y recibi: {msg}")

	print("Soy el cliente y voy a enviar")

	skt.send_with_size("Hola servidor!")

	skt.close()

if __name__ == '__main__':
	main()
