from modules.ServerHandler.server_handler import Server


def main():
    server = Server()
    server.serve()
    

if __name__ == '__main__':
    main()