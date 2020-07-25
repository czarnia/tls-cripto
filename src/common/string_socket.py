import socket
import ssl

DEFAULT_SIZE = 20

'''A kind and nice socket that sends and receives strings'''
class StringSocket(object):
    def __init__(self, skt=None):
        '''Initializer for the StringSocket, if no socket is given,
        a new one of type TCP is created'''
        if (skt):
            self.skt = skt
        else:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def use_ssl_client(self, server_cert, client_cert, client_key, server_sni_hostname):
        '''Uses ssl for the client'''
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
        context.load_cert_chain(certfile=client_cert, keyfile=client_key)
        self.skt = context.wrap_socket(self.skt, server_side=False, server_hostname=server_sni_hostname)

    def accept_ssl(self, server_cert, server_key, client_certs):
        '''Accepts a new connectio using SSL, a new StringSocket and
        the connected address is returned'''
        try:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_cert_chain(certfile=server_cert, keyfile=server_key)
            context.load_verify_locations(cafile=client_certs)

            new_skt, addr = self.skt.accept()
            return StringSocket(context.wrap_socket(new_skt, server_side=True)), addr
        except socket.timeout:
            return None, None

    def connect(self, host, port):
        '''Connects the socket to a given port and host'''
        self.skt.connect((host, port))

    def bind(self, host, port):
        '''Binds the socket to a giver port and host'''
        self.skt.bind((host, port))

    def listen(self, queued_connections=None):
        '''Sets the socket to listening mode'''
        if queued_connections:
            self.skt.listen(queued_connections)
        else:
            self.skt.listen()

    def accept(self):
        '''Accepts a new connection, a new StringSocket and
        the connected address is returned'''
        try:
            new_skt, addr = self.skt.accept()
            return StringSocket(new_skt), addr
        except socket.timeout:
            return None, None

    def sendall(self, msg):
        '''Sends the full string msg'''
        self.skt.sendall(msg.encode())

    def send_with_size(self, msg, max_digits = DEFAULT_SIZE):
        '''Sends the size of the string msg and then the full msg'''
        self.skt.sendall(str(len(msg)).zfill(max_digits).encode())
        self.skt.sendall(msg.encode())

    def receiveall(self, msg_len):
        '''Receives and string of size msg_len'''
        msg = ""
        while len(msg) < msg_len:
            chunk = self.skt.recv(msg_len-len(msg))
            if not chunk:
                raise RuntimeError('Lal')
            msg = msg + chunk.decode('UTF-8', 'ignore')
        return msg

    def receive_with_size(self, size_field_size = DEFAULT_SIZE):
        '''Receives the size of the msg with size size_field_size and
        after the msg, the later is returned'''
        field_size = self.receiveall(size_field_size)
        return self.receiveall(int(field_size))

    def close(self):
        '''Closes the socket immediately'''
        self.skt.shutdown(socket.SHUT_RD)
        self.skt.close()

    def settimeout(self, time):
        '''Sets a timeout of time time for the socket'''
        self.skt.settimeout(time)