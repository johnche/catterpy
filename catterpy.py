import socket, argparse, sys
from _thread import start_new_thread


class ArgparseHelp(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


parser = ArgparseHelp(description='Catterpy, simplified netcat in python')
parser.add_argument('-l', action='store_true', dest='server_socket', default=False,
        help='Specifies catterpy to listen for incoming connection.')
parser.add_argument('-i', '--ip', type=str,
        help='Sets the host catterpy connects to')
parser.add_argument('port', metavar='PORT', type=int,
        help='Sets server/client port, depending on the -l flag is set')
args = parser.parse_args()


def user_input(socket_instance):
    while True:
        socket_instance.send((input() + '\n').encode('utf-8'))


def tcp_socket_client(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print('Trying %s' % socket.gethostbyname(address[0]))
        sock.connect(address)
        print('Connected to %s' % address[0])
        start_new_thread(user_input, (sock,))
        while True:
            data = sock.recv(1024)
            if not data: break
            print(data.decode('utf-8').strip())
    except socket.error as e:
        print("Connection failed: %s" % str(e))
    finally:
        sock.close()
        print("Socket closed")
        sys.exit(0)


def tcp_socket_server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(address)
        sock.listen(1)
        print('Listening at %s %s' % address)
        conn, addr = sock.accept()
        print('%s:%s connected' % addr)
        start_new_thread(user_input, (conn,))
        with conn:
            while True:
                data = conn.recv(1024)
                if not data: break
                print(data.decode('utf-8').strip())
    except socket.error as e:
        print('Error: %s' % str(e))
    finally:
        sock.close()
        print('Socket closed')
        sys.exit(0)


def main():
    if args.server_socket:
        ip = '0.0.0.0'
        if args.ip:
            ip = args.ip
        tcp_socket_server((ip, args.port))
    else:
        tcp_socket_client((args.ip, args.port))


if __name__ == "__main__":
    main()

